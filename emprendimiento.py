from flask import Blueprint, render_template, request, redirect, session
from userLogic import UserLogic
from userObj import UserObj
from inversorLogic import inversorLogic
from inversorObj import inversorObj
from emprendedorLogic import emprendedorLogic
from emprendedorObj import emprendedorObj
from emprendimientoLogic import emprendimientoLogic
from ofertaLogic import ofertaLogic
from guardadosLogic import guardadosLogic

emprendimiento = Blueprint(
    "emprendimiento", __name__, template_folder="Templates", static_folder="static"
)


@emprendimiento.route("/quienes_somosInv", methods=["GET", "POST"])
def quienesSomosInv():
    idEmprendimiento = session["empId"]
    logic = emprendimientoLogic()
    if request.method == "GET":
        data = logic.getAllFundadores(idEmprendimiento)
        data2 = logic.getHistoria(idEmprendimiento)
        data3 = logic.getDatosGeneralesById(idEmprendimiento)
        data4 = logic.getDescripcion(idEmprendimiento)
        logic.saveImagesFundadores(idEmprendimiento)
        return render_template(
            "quienes_somos.html",
            data=data,
            data2=data2,
            data3=data3,
            data4=data4,
            message="",
            vistaEmprendimiento=True,
        )


@emprendimiento.route("/quienes_somos", methods=["GET", "POST"])
def quienesSomos():
    logic = emprendimientoLogic()
    message = ""
    verdadero = False
    idEmprendimiento = session["emprendimiento"]

    # Vista
    vistaEmprendimiento = True

    if request.method == "GET":
        # vista Inversionista
        vistaEmprendimiento = False
        data = logic.getAllFundadores(idEmprendimiento)
        data2 = logic.getHistoria(idEmprendimiento)
        data3 = logic.getDatosGeneralesById(idEmprendimiento)
        data4 = logic.getDescripcion(idEmprendimiento)
        logic.saveImagesFundadores(idEmprendimiento)
        return render_template(
            "quienes_somos.html",
            data=data,
            data2=data2,
            data3=data3,
            data4=data4,
            message=message,
            vistaEmprendimiento=vistaEmprendimiento,
        )
    elif request.method == "POST":
        formId = int(request.form["formId"])
        # INSERTAR
        if formId == 1:
            user = request.form["user"]
            rol = 3
            logicUsuario = UserLogic()
            logicEmpre = emprendimientoLogic()
            # Comprobando si existe
            existeUsuario = logicUsuario.checkUserInUsuario(user, rol)
            if existeUsuario:
                # compruebo si ya lo habian insertado
                alredyInseted = logicEmpre.checkUserAlredyExist(user, idEmprendimiento)
                if alredyInseted is False:
                    rows = logic.insertNewFundador(user, idEmprendimiento)
                    data = logic.getAllFundadores(idEmprendimiento)
                    data2 = logic.getHistoria(idEmprendimiento)
                    logicEmpre.insertNotificationFundador(user, idEmprendimiento)
                    message = "Se ha agregado al fundador"
                    return render_template(
                        "quienes_somos.html", data=data, data2=data2, message=message
                    )
                else:
                    data = logic.getAllFundadores(idEmprendimiento)
                    data2 = logic.getHistoria(idEmprendimiento)
                    message = (
                        "El usuario ya se encuentra asignado a este emprendimiento."
                    )
                    return render_template(
                        "quienes_somos.html", data=data, data2=data2, message=message
                    )
            else:
                data = logic.getAllFundadores(idEmprendimiento)
                data2 = logic.getHistoria(idEmprendimiento)
                message = "El usuario o emprendimiento seleccionado no existe. Pruebe de nuevo"
                return render_template(
                    "quienes_somos.html", data=data, data2=data2, message=message
                )
        # ELIMINAR
        elif formId == 2:
            id = int(request.form["id"])
            logic.deleteFundador(id)
            message = "Se ha eliminado un fundador"
            data = logic.getAllFundadores(idEmprendimiento)
            data2 = logic.getHistoria(idEmprendimiento)
            return render_template(
                "quienes_somos.html", data=data, data2=data2, message=message
            )
        # MODIFICAR HISTORIA
        elif formId == 3:
            historia = request.form["historia"]
            logic.updateHistoria(idEmprendimiento, historia)
            data = logic.getAllFundadores(idEmprendimiento)
            data2 = logic.getHistoria(idEmprendimiento)
            return render_template(
                "quienes_somos.html", data=data, data2=data2, message=message
            )


@emprendimiento.route("/informacion", methods=["GET", "POST"])
def informacion():
    vistaInversor = False
    logic = emprendimientoLogic()
    message = ""
    mostrar = False
    logicOferta = ofertaLogic()

    idEmprendimiento = session["emprendimiento"]
    if request.method == "GET":
        data = logic.getContactos(idEmprendimiento)
        data2 = logic.getInfoFinanciera(idEmprendimiento)
        data3 = logic.getDatosGeneralesById(idEmprendimiento)
        data4 = logic.getDescripcion(idEmprendimiento)
        ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
        ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)

        return render_template(
            "informacion.html",
            data=data,
            data2=data2,
            data3=data3,
            data4=data4,
            message=message,
            vistaEmprendedor=True,
            vistaEmprendimiento=True,
            ofertas=ofertas,
            ultima_oferta=ultima_oferta,
        )
    elif request.method == "POST":
        vistaEmprendedor = True
        formId = int(request.form["formId"])
        data = logic.getContactos(idEmprendimiento)
        data2 = logic.getInfoFinanciera(idEmprendimiento)
        ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
        ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
        # UPDATE INFO FINANCIERA
        if formId == 1:
            fecha_fundacionOld = request.form["fecha_fundacionx"]
            inversion_inicialOld = request.form["inversion_inicialx"]
            venta_año_anteriorOld = request.form["venta_año_anteriorx"]
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                mostrar=True,
                vistaEmprendedor=True,
                fecha_fundacionUpx=fecha_fundacionOld,
                inversion_inicialUpx=inversion_inicialOld,
                venta_año_anteriorUpx=venta_año_anteriorOld,
                data=data,
                data2=data2,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )
        if formId == 2:
            fecha_fundacion = request.form["fecha_fundacionUP"]
            inversion_inicial = request.form["inversion_inicialUP"]
            venta_año_anterior = request.form["venta_año_anteriorUP"]
            logic.updateInfoFinanciera(
                idEmprendimiento,
                inversion_inicial,
                fecha_fundacion,
                venta_año_anterior,
            )
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                mostrar=False,
                vistaEmprendedor=True,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )
        # UPDATE CONTACTOS
        if formId == 3:
            emailOld = request.form["emailx"]
            telefonoOld = request.form["telefonox"]
            facebookOld = request.form["facebookx"]
            instagramOld = request.form["instagramx"]
            youtubeOld = request.form["youtubex"]
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                mostrar1=True,
                vistaEmprendedor=True,
                emailUpx=emailOld,
                telefonoUpx=telefonoOld,
                facebookUpx=facebookOld,
                instagramUpx=instagramOld,
                youtubeUpx=youtubeOld,
                data=data,
                data2=data2,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )
        if formId == 4:
            email = request.form["emailUP"]
            telefono = request.form["telefonoUP"]
            facebook = request.form["facebookUP"]
            instagram = request.form["instagramUP"]
            youtube = request.form["youtubeUP"]
            logic.updateContactos(
                idEmprendimiento, email, telefono, facebook, instagram, youtube
            )
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                mostrar1=False,
                vistaEmprendedor=True,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )

        # Agrega un registro al historial
        if formId == 5:
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                mostrar2=True,
                vistaEmprendedor=True,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )
        if formId == 6:
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            especificaciones = request.form["especificaciones"]
            oferta = float(request.form["oferta"])
            porcentaje = float(request.form["porcentaje"])
            logicOferta.insertOferta(
                especificaciones, oferta, porcentaje, idEmprendimiento
            )
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                vistaEmprendedor=True,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )
        # Delete
        if formId == 7:
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            id_historial = request.form["id_historial"]
            logicOferta.deleteHistorial(id_historial)
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                vistaEmprendedor=True,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )

        # Update
        if formId == 8:
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            id_historial = request.form["id_historial"]
            especificaciones = request.form["especificaciones"]
            oferta = float(request.form["oferta"])
            porcentaje = float(request.form["porcentaje"])
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            data3 = {
                "id_historial": id_historial,
                "especificaciones": especificaciones,
                "oferta": oferta,
                "porcentaje": porcentaje,
            }
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                vistaEmprendedor=True,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
                data3=data3,
                mostrar3=True,
            )
        if formId == 9:
            data = logic.getContactos(idEmprendimiento)
            data2 = logic.getInfoFinanciera(idEmprendimiento)
            id_historial = request.form["id_historial"]
            especificaciones = request.form["especificaciones"]
            oferta = float(request.form["oferta"])
            porcentaje = float(request.form["porcentaje"])
            logicOferta.updateHistorial(
                especificaciones, oferta, porcentaje, id_historial
            )
            ofertas = logicOferta.getAllOfertasByIdEmprendimiento(idEmprendimiento)
            ultima_oferta = logicOferta.getLastOferta(idEmprendimiento)
            return render_template(
                "informacion.html",
                data=data,
                data2=data2,
                vistaEmprendedor=True,
                vistaEmprendimiento=True,
                ofertas=ofertas,
                ultima_oferta=ultima_oferta,
            )

