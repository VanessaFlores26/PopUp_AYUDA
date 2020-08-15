from emprendimientoLogic import emprendimientoLogic
from flask import Blueprint, Flask, render_template, request, redirect, session
import mysql.connector
from mysql.connector import Error

emprendimientoInicio = Blueprint(
    "emprendimientoInicio",
    __name__,
    static_folder="static",
    template_folder="Templates",
)


@emprendimientoInicio.route(
    "/emprendimientoInicioInversionista", methods=["GET", "POST"]
)
def getInformacion():
    if session["empId"] == "":
        idEmprendimiento = int(request.form["empId"])
        session["empId"] = idEmprendimiento
        print(idEmprendimiento)
    else:
        idEmprendimiento = session["empId"]
    logic = emprendimientoLogic()
    data = logic.getDatosGeneralesById(idEmprendimiento)
    if request.method == "GET":
        return render_template(
            "emprendimientoInicio.html",
            data=data,
            message="",
            vistaEmprendimiento=True,
        )
    elif request.method == "POST":
        return render_template(
            "emprendimientoInicio.html",
            data=data,
            message="",
            vistaEmprendimiento=True,
        )


@emprendimientoInicio.route("/emprendimientoInicio", methods=["GET", "POST"])
def getInformacionGeneral():
    logic = emprendimientoLogic()
    message = ""
    data2 = None
    idEmprendimiento = session["emprendimiento"]
    verdadero = False
    data = logic.getDatosGeneralesById(idEmprendimiento)
    logic.saveImagesEmprendimiento(idEmprendimiento)

    # vista
    vistaEmprendimiento = True

    if request.method == "GET":
        # Si es False - Vista emprendedor
        vistaEmprendimiento = False
        return render_template(
            "emprendimientoInicio.html",
            data=data,
            message=message,
            vistaEmprendimiento=vistaEmprendimiento,
        )

    elif request.method == "POST":
        formId = int(request.form["formId"])

        if formId == 1:
            verdadero = True
            descripcion = request.form["descripcion"]
            eslogan = request.form["eslogan"]
            nombre = request.form["nombre"]
            nombre_foto = request.form["nombre_foto"]
            video = request.form["video"]
            verdadero = True
            data2 = {
                "descripcion": descripcion,
                "eslogan": eslogan,
                "nombre": nombre,
                "nombre_foto": nombre_foto,
                "video": video,
            }
        elif formId == 2:
            descripcion = request.form["descripcion"]
            eslogan = request.form["eslogan"]
            nombre = request.form["nombre"]
            foto = request.files["fileToUpload"]
            nombre_foto = foto.filename
            video = request.form["video"]

            if foto.filename == "":
                logic.updateDatosGeneralesWithoutFoto(
                    idEmprendimiento, descripcion, eslogan, nombre, video,
                )
            else:
                binary_foto = foto.read()
                logic.updateDatosGeneralesWithFoto(
                    idEmprendimiento, descripcion, eslogan, nombre, binary_foto, video,
                )
            data = logic.getDatosGeneralesById(idEmprendimiento)
            logic.saveImagesEmprendimiento(idEmprendimiento)

        return render_template(
            "emprendimientoInicio.html", data=data, verdadero=verdadero, data2=data2
        )
