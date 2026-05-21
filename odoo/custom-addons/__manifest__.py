<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>

        <!-- ── Vista lista ─────────────────────────────────────────────── -->
        <record id="view_asistencia_list" model="ir.ui.view">
            <field name="name">odoo_ute.asistencia.list</field>
            <field name="model">odoo_ute.asistencia</field>
            <field name="arch" type="xml">
                <list string="Asistencias">
                    <field name="alumno_id"/>
                    <field name="curso_id"/>
                    <field name="fecha"/>
                    <field name="presente"/>
                </list>
            </field>
        </record>

        <!-- ── Vista formulario ───────────────────────────────────────── -->
        <record id="view_asistencia_form" model="ir.ui.view">
            <field name="name">odoo_ute.asistencia.form</field>
            <field name="model">odoo_ute.asistencia</field>
            <field name="arch" type="xml">
                <form string="Registro de Asistencia">
                    <sheet>
                        <group>
                            <group string="Datos de la asistencia">
                                <field name="alumno_id"/>
                                <field name="curso_id"/>
                                <field name="fecha"/>
                                <field name="presente"/>
                            </group>
                        </group>
                        <group string="Observaciones">
                            <field name="observaciones" nolabel="1"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- ── Acción ─────────────────────────────────────────────────── -->
        <record id="action_asistencia" model="ir.actions.act_window">
            <field name="name">Asistencias</field>
            <field name="res_model">odoo_ute.asistencia</field>
            <field name="view_mode">list,form</field>
        </record>

    </data>
</odoo>
