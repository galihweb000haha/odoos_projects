odoo.define('pos_basic.galih_custom_chrome', function(require){
    "use strict";
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var chrome = require('point_of_sale.chrome');
    var Chrome = chrome.Chrome;

    var gui = require('point_of_sale.gui');
    var Gui = gui.Gui;

    var PosDB = require('point_of_sale.DB');

    var models = require('point_of_sale.models');

    var core = require('web.core');
    var _t = core._t;

    var CompanyLogoWidget = PosBaseWidget.extend({
        template: 'CompanyLogoWidget',
        init: function(parent, options) {
            options = options || {};
            this._super(parent, options);
        },
        get_company_logo: function () {
            var self = this;
            return self.pos.company_logo.src;
        },
        renderElement: function(){
            var self = this;
            this._super();             
        },
    })

    var SalesPersonWidget = PosBaseWidget.extend({
        template: 'SalesPersonWidget',
        init: function(parent, options){
            options = options || {};
            this._super(parent,options);
        },
        get_name: function(){
            var user = this.pos.get_salesperson();
            return (user ? user.name : '');
        },
    });

    SalesPersonWidget.include({
        renderElement: function(){
            var self = this;
            this._super();             
            this.el.addEventListener('click', () => self.click_salesperson());
        },
        click_salesperson: function(){
            if(!this.pos.config.module_pos_hr) {
                return; 
            }
            var self = this;

            // gui.select_salesperson will return promise
            this.gui.select_salesperson({
                'security': true,
                'current_employee': this.pos.get_salesperson(),
                'title': _t('Change Salesperson')
            }).then(function(employee){
                self.pos.set_salesperson(employee);
                self.chrome.widget.salesperson.renderElement();
                self.renderElement();
            })
        }
    });

    PosDB.include({
        set_salesperson: function(salesperson) {
            this.save('salesperson', salesperson || null);
        },
        get_salesperson: function() {
            return this.load('salesperson');
        }
    });

    models.PosModel = models.PosModel.extend({
        get_salesperson: function(){
            if (this.db.load('pos_session_id') !== this.pos_session.id) {
                this.set_salesperson(this.employee);
            }

            return this.db.get_salesperson() || this.get('salesperson') || this.employee;
        },
        
        set_salesperson: function(employee){
            this.set('salesperson', employee);
            this.db.set_salesperson(employee);
        }
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_as_JSON: function () {
            var data = _super_order.export_as_JSON.apply(this, arguments)
            data.salesperson_id = this.pos.get_salesperson() ? this.pos.get_salesperson().id : null;

            return data;
        },
        export_for_printing: function () {
            var salesperson = this.pos.get_salesperson();
            var data = _super_order.export_for_printing.apply(this, arguments)
            data.salesperson = salesperson ? salesperson.name : "";

            return data
        }
    });

    Chrome.include({
        build_widgets: function () {
            this.widgets.push(
                {
                    'name': 'salesperson',
                    'widget': SalesPersonWidget,
                    'replace': '.placeholder-SalesPersonWidget',
                },
                {
                    'name': 'companylogo',
                    'widget': CompanyLogoWidget,
                    'replace': '.placeholder-CompanyLogoWidget'
                },
            );
            this._super();
        }
    });

    Gui.include({
        select_salesperson: function(options) {
            var self = this;
            var list = [];

            this.pos.employees.forEach(function(salesperson){
                // if only_managers is false or role of salesperson is manager then push it to list
                if (!options.only_managers || salesperson.role === 'manager') {
                    list.push({
                        'label': salesperson.name,
                        'item': salesperson
                    });
                }

            });

            var prom = new Promise(function(resolve, reject) {
                self.show_popup('selection', {
                    title: options.title || _t('Select Salesperson'),
                    list: list,
                    confirm: resolve,
                    cancel: reject,
                    is_selected: function(salesperson) {
                        return salesperson === self.pos.get_salesperson();
                    },
                });
            });

            return prom.then(function (employee) {
                return self.ask_password(employee.pin).then(function(){
                    return employee;
                });
            });
        }
    });


    return {
        'SalesPersonWidget':SalesPersonWidget,
        'CompanyLogoWidget':CompanyLogoWidget,
    }
}) 

