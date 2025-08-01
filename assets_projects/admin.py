from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models.asset import Asset
from .models.project import Project
from .models.cost import ProjectCost
from django.contrib.contenttypes.admin import GenericTabularInline
from core.models import Attachment


class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 0


# Resources for import-export
class AssetResource(resources.ModelResource):
    class Meta:
        model = Asset
        fields = ('id', 'name', 'asset_type', 'price', 'purchase_date', 'lifespan', 'farm')

class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'name', 'parent_project', 'description', 'address', 'farm')

class ProjectCostResource(resources.ModelResource):
    class Meta:
        model = ProjectCost
        fields = ('id', 'name', 'project', 'asset','cost_type', 'amount', 'description', 'farm')

# Custom Filters
class HighValueAssetFilter(SimpleListFilter):
    title = _('High Value Assets')
    parameter_name = 'high_value'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('High Value (> $10,000)')),
            ('no', _('Regular Value')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(price__gt=10000)
        if self.value() == 'no':
            return queryset.filter(price__lte=10000)

class RecentProjectFilter(SimpleListFilter):
    title = _('Recently Created')
    parameter_name = 'recent'

    def lookups(self, request, model_admin):
        return (
            ('30days', _('Last 30 days')),
            ('90days', _('Last 90 days')),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        
        if self.value() == '30days':
            return queryset.filter(created_at__gte=timezone.now()-timedelta(days=30))
        if self.value() == '90days':
            return queryset.filter(created_at__gte=timezone.now()-timedelta(days=90))

class FarmFilter(SimpleListFilter):
    title = _('Farm')
    parameter_name = 'farm'

    def lookups(self, request, model_admin):
        from core.models import Farm
        return Farm.objects.values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(farm_id=self.value())
        return queryset

# Admin Classes
class ProjectCostInline(admin.TabularInline):
    model = ProjectCost
    extra = 0
    classes = ('collapse',)
    fields = ('name', 'amount', 'asset', 'description', 'created_at', 'farm')
    readonly_fields = ('created_at',)
    show_change_link = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(farm=request.user.active_farm)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "farm":
            if not request.user.is_superuser:
                kwargs["queryset"] = db_field.remote_field.model.objects.filter(id=request.user.active_farm.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Asset)
class AssetAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AssetResource
    list_display = ('id', 'name', 'asset_type', 'price','asset_code' ,'purchase_date', 'primary_project', 'farm', 'supplier', 'created_at')
    list_filter = (HighValueAssetFilter, 'asset_type', 'purchase_date', 'primary_project', FarmFilter)
    search_fields = ('name', 'description', 'supplier__name', 'farm__name', 'primary_project__name')
    list_per_page = 20
    date_hierarchy = 'purchase_date'
    list_select_related = ('farm', 'supplier', 'primary_project')
    filter_horizontal = ('shared_projects',)

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'asset_type', 'description', 'farm')
        }),
        (_('Financial Information'), {
            'fields': ('price', 'purchase_date', 'lifespan'),
            'classes': ('collapse',)
        }),
        (_('Relationships'), {
            'fields': ('supplier', 'primary_project', 'shared_projects'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_agricultural']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(farm=request.user.active_farm)

    def save_model(self, request, obj, form, change):
        if not obj.farm_id:
            obj.farm = request.user.active_farm
        elif not request.user.is_superuser and obj.farm != request.user.active_farm:
            raise PermissionDenied("Cannot assign to different farm")
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "farm":
            if not request.user.is_superuser:
                kwargs["queryset"] = db_field.remote_field.model.objects.filter(id=request.user.active_farm.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def mark_as_agricultural(self, request, queryset):
        updated = queryset.update(asset_type='agricultural')
        self.message_user(request, _("Successfully marked %d assets as agricultural") % updated)
    mark_as_agricultural.short_description = _("Mark selected assets as agricultural")


class PrimaryAssetInline(admin.TabularInline):
    model = Asset
    fk_name = 'primary_project'  
    extra = 0
    readonly_fields = ('name', 'asset_type', 'price', 'purchase_date')
    can_delete = False
    show_change_link = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('primary_project')


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProjectResource

    list_display = (
        'id', 'name', 'project_number', 'farm', 'parent_project',
        'start_date', 'end_date', 'created_at',
        'cost_count', 'total_cost_display'  # ✅ Use method instead of raw property
    )

    list_filter = (
        RecentProjectFilter, 'created_at', 'parent_project', FarmFilter
    )

    search_fields = ('name', 'description', 'address', 'farm__name')
    list_per_page = 20
    date_hierarchy = 'created_at'
    inlines = [ProjectCostInline, AttachmentInline, PrimaryAssetInline]
    raw_id_fields = ('parent_project',)

    readonly_fields = ('project_number', 'project_code', 'total_cost_display')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'farm', 'project_number', 'project_code', 'parent_project', 'description')
        }),
        (_('Timeline'), {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
        (_('Location'), {
            'fields': ('address',),
            'classes': ('collapse',)
        }),
    )

    actions = ['duplicate_project']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(farm=request.user.active_farm)

    def save_model(self, request, obj, form, change):
        if not obj.farm_id:
            obj.farm = request.user.active_farm
        elif not request.user.is_superuser and obj.farm != request.user.active_farm:
            raise PermissionDenied("Cannot assign to different farm")
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "farm":
            if not request.user.is_superuser:
                kwargs["queryset"] = db_field.remote_field.model.objects.filter(id=request.user.active_farm.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def duplicate_project(self, request, queryset):
        for project in queryset:
            project.pk = None
            project.name = f"Copy of {project.name}"
            project.save()
        self.message_user(request, _("Selected projects were duplicated successfully"))
    duplicate_project.short_description = _("Duplicate selected projects")

    def cost_count(self, obj):
        return obj.costs.count()
    cost_count.short_description = _('Cost Items')

    def total_cost_display(self, obj):
        return obj.total_costs  # assume this is a @property or annotated value
    total_cost_display.short_description = _('Total Cost')


@admin.register(ProjectCost)
class ProjectCostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProjectCostResource
    list_display = ('id', 'name', 'project', 'farm', 'amount','cost_type', 'asset', 'created_at')
    list_filter = ('project', FarmFilter,'cost_type', 'created_at', 'asset')
    search_fields = ('name', 'description', 'project__name', 'farm__name')
    list_per_page = 20
    date_hierarchy = 'created_at'
    raw_id_fields = ('project', 'asset')
    list_select_related = ('project', 'farm', 'asset')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'project', 'farm', 'amount', 'description')
        }),
        (_('Asset Information'), {
            'fields': ('asset',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(farm=request.user.active_farm)

    def save_model(self, request, obj, form, change):
        if not obj.farm_id:
            obj.farm = request.user.active_farm
        elif not request.user.is_superuser and obj.farm != request.user.active_farm:
            raise PermissionDenied("Cannot assign to different farm")
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "farm":
            if not request.user.is_superuser:
                kwargs["queryset"] = db_field.remote_field.model.objects.filter(id=request.user.active_farm.id)
        elif db_field.name == "project":
            if not request.user.is_superuser:
                kwargs["queryset"] = db_field.remote_field.model.objects.filter(farm=request.user.active_farm)
        elif db_field.name == "asset":
            if not request.user.is_superuser:
                kwargs["queryset"] = db_field.remote_field.model.objects.filter(farm=request.user.active_farm)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)