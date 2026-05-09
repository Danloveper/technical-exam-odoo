# Ticket#1

1. __Causa__:   Los pagos se calculaban respecto al primer pago porque utilizaba min

2. __solucion__: Calcular el pago mas lejano con ``max``para ajustar los dias

3. __impacto__: Tiene en cuenta el plazo a partir del primer pago

# Ticket#2

1. __Causa__:   La actualización de metricas de pagos en las facturas de cliente solo se actualiza diariamente por un cron 

2. __solucion__: Heredar la función que confirma el pago para añadir la función que actualiza metricas

3. __impacto__: Ya no es necesario esperar al siguiente día para obtener la información actualizada, sino que se realiza automaticamente al registrar pagos 

# Parte 2

El nuevo enfoque permite a los usuarios pertenecientes al grupo group_account_manager (director de Contabilidad) actualizar las metricas de pago de facturas del cliente mediante una factura

# Parte 3

1. __Problemas/Mejoras__:

    * Faltan las importaciones de odoo ``from odoo import _, api, fields, models`` para que el interprete puede acceder a los modelos, metodos y campos del ORM. 

    * El campo ``average_pay_time`` se agrega en las dependencias, pero no genera ningun impacto en el calculo. Se debe quitar del depends.

    * 

2. __Impacto risk_level y depends__: Guardar en la base de datos el valor del calculo, es decir que cada vez que se ingrese a la vista o se realice un llamado (self.env['res.partner']) al modelo para un reporte o consulta se ejecutara la función ``_compute_risk_level``. El calculo es sencillo sin embargo puede traer lentitud en el servicio cuando hace referencia a muchos registros.

    Ademas el depends ``@api.depends('percentage_invoices_on_time', 'average_pay_time', 'is_black_list')`` indica que cada actualización de esos campos genera recalcular la función, teniendo encuenta que hay el campo ``average_pay_time`` no afecta en el calculo real.

    Si el campo es meramente informativo se sugiere quitar el ``store=True``, eliminar el campo ``average_pay_time`` del depends 

3. __Contexto i18n message_post__: Se debe agregar en las importaciones ``_`` para poder generar las traducciones, de lo contrario el usuario visualiza el mensaje en Ingles, a continuación se presenta la actualización: ``_('Risk notification sent to %s. Current level: %s', partner.name, partner.risk_level)``. El archivo correspondiente a traducción al español es ``es_CO.po``

4. __Envio masivo_de mails__: Depende si la acción es simplemente a nivel de correo o se requiere utilizar los mensajes de seguimiento en el modelo. Para lo cual se asume utiliza la misma funcionalidad de ``action_send_risk_notification``.  Se propone crear un wizard donde pueda registrar varios partner (campo many2many o one2many) y con un boton ejecute dentro de el modelo ``res.partner`` la función ``action_send_risk_notification``. Ya que ``self`` contendra varios registros y en la acción ya se recorre uno a uno con ``for partner in self:```no hay lio.


# Parte 4

1. __Reporte__: 

    * __QUE__: Crear un reporte que permita visualizar la información de los clientes con respecto a los pagos, ademas de poder filtrar por tipo de riesgo o porcentaje.

    * __POR QUE__: El equipo de Cartera puede analizar mas a detalle la información del cliente puesto que se puede agregar información de otros modelos como el de facturas. Ademas si tienen alguna plantilla de excel que permita plasmar la misma información que en el sistema tambien se puede migrar.

    * __COMO__: Desarrollo de ``report`` tipo ``xlsx`` donde se extraiga la información relevante que el equipo de cartera considere le permita hacer nuevos estudios y balances. Se sugiere utilizar la libreria de ``pandas`` para optimizar las consultas a los modelos junto con el metodo ``search_read`` del ORM para extraer solo los campos necesarios; y de esta forma se garantizar un flujo eficiente en el reporte

    * __Riesgo__: Posible saturación en el servicio por mala parametrización de domains y calculos.

1. __Vista Kaban__: 

    * __QUE__: Diseñar vista kanban para visualizar información de pagos facturas respecto a los clientes

    * __POR QUE__: