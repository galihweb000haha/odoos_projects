from odoo import api, fields, models, _
from odoo.exceptions import AccessDenied

TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]

class HelpdeskMergeTicket(models.TransientModel):
    _name = 'helpdesk.merge.ticket'
    _description = 'Merge Tickets'
        
    ticket_target_id = fields.Many2one('helpdesk.ticket', string='Ticket Target', index=True)
    merge_ids = fields.Many2many('helpdesk.ticket')
    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', index=True)
    user_id = fields.Many2one(
        'res.users', string='Assigned to', compute='_compute_user_and_stage_ids', store=True,
        readonly=False, tracking=True,
        domain=lambda self: [('groups_id', 'in', self.env.ref('helpdesk.group_helpdesk_user').id)])
    tag_ids = fields.Many2many('helpdesk.tag', string='Tags')
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', string="Ticket Type")
    priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='0')
    stage_id = fields.Many2one('helpdesk.stage', string='Stage', ondelete='restrict', tracking=True,
                               group_expand='_read_group_stage_ids', copy=False,
                               index=True, domain="[('team_ids', '=', team_id)]")
    partner_id = fields.Many2one('res.partner', string='Customer')
    description = fields.Text()

    @api.onchange('ticket_target_id')
    def _onchange_ticket_target(self):
        """
            check selected tickets id to avoid merging the same ticket
            assigning all fields with record on selected id 
        """
        # avoid ticket target same as the selected ticket above
        for ticket_id in self.merge_ids.ids:
            if ticket_id == self.ticket_target_id.id:
                raise AccessDenied(
                    _("The target ticket cannot be the same as the selected ticket above !")
                )

        self.team_id = self.ticket_target_id.team_id
        self.user_id = self.ticket_target_id.user_id
        self.ticket_type_id = self.ticket_target_id.ticket_type_id
        self.partner_id = self.ticket_target_id.partner_id
        self.priority = self.ticket_target_id.priority
        
        
    @api.model
    def default_get(self, fields):
        """
            get selected ids of ticket
            set merge ids with selected ids
        """
        res = super(HelpdeskMergeTicket, self).default_get(fields)
        select_ids = self.env.context.get('active_ids',[])
        selected_items = self.env['helpdesk.ticket'].browse(select_ids)
        res.update({
            'merge_ids': [(6, _, selected_items.ids)]
        })

        return res

    def merge_tickets(self):
        """
            validate and merge tickets
        """
        # avoid merging solved ticket
        for ticket in self.merge_ids:
            if ticket.stage_id.is_close or self.ticket_target_id.stage_id.is_close :
                raise AccessDenied(
                    _("Cannot merge solved ticket / the the stage of ticket is closed")
                )
        # merge description 
        self.description = " -> {name}: {description} \n".format(name = self.ticket_target_id.name, description = self.ticket_target_id.description or '')

        for ticket in self.merge_ids:
            txt = " -> {name}: {description} \n".format(name = ticket.name, description = ticket.description or '')
            self.description += txt

        # merge followers
        ticket_target_partner = self.ticket_target_id.message_follower_ids.partner_id
        merge_ids_partner = self.merge_ids.message_follower_ids.partner_id
        new_partner = merge_ids_partner - ticket_target_partner + ticket_target_partner
        self.ticket_target_id.message_subscribe(new_partner.mapped('id'))

        self.partner_id = self.ticket_target_id.partner_id
        self.ticket_target_id.write({
            'name': self.ticket_target_id.name,
            'user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'ticket_type_id': self.ticket_type_id.id,
            'priority': self.priority,
            'partner_id': self.partner_id.id,
            'description': self.description,
        })
        
        # archive merged ticket
        self.merge_ids.action_archive()