from django.contrib import admin

from helpdesk.models import (
    Queue, Ticket, FollowUp, PreSetReply, KBCategory,
    EscalationExclusion, EmailTemplate, KBItem,
    TicketChange, Attachment, IgnoreEmail,
    CustomField, UserSettings
)


class QueueAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'email_address', 'locale')
    
    raw_id_fields = (
        'group',
    )


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'queue', 'title', 'status', 'assigned_to', 'submitter_email',)
    date_hierarchy = 'created'
    list_filter = ('assigned_to', 'status', 'queue',)
    raw_id_fields = ('assigned_to',)


class TicketChangeInline(admin.StackedInline):
    model = TicketChange


class AttachmentInline(admin.StackedInline):
    model = Attachment


class FollowUpAdmin(admin.ModelAdmin):
    inlines = [TicketChangeInline, AttachmentInline]


class KBItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'last_updated',)
    list_display_links = ('title',)


class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'data_type')


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name', 'heading', 'locale')
    list_filter = ('locale', )


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    
    search_fields = (
        'user__username',
        'user__email'
    )
    
    exclude = (
        'settings_pickled',
    )
    
    raw_id_fields = (
        'user',
    )
    
    readonly_fields = (
        'settings_pickled_str',
    )
    
    def settings_pickled_str(self, obj=None):
        if not obj:
            return ''
        settings = obj.settings
        return '<table>' + ''.join(
            '<tr><th>%s</th><td>%s</td></tr>' % (k, settings[k])
            for k in sorted(settings.keys())
        ) + '</table>'
    settings_pickled_str.allow_tags = True


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Queue, QueueAdmin)
admin.site.register(FollowUp, FollowUpAdmin)
admin.site.register(PreSetReply)
admin.site.register(EscalationExclusion)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(KBCategory)
admin.site.register(KBItem, KBItemAdmin)
admin.site.register(IgnoreEmail)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)
