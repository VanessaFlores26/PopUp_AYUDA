from flask import Blueprint, Flask, render_template, request, redirect, session
import mysql.connector
from mysql.connector import Error
from emprendedorLogic import emprendedorLogic
from emprendimientoLogic import emprendimientoLogic


emprendedorProfile = Blueprint(
    "emprendedorProfile", __name__, static_folder="static", template_folder="Templates",
)


@emprendedorProfile.route("/emprendedorProfile", methods=["GET", "POST"])
def ProfileEmp():
    try:
        logic = emprendedorLogic()
        logicEmprendimiento = emprendimientoLogic()
        user = session["user"]
        idUsuario = int(user["id"])
        data = logic.getDatosGeneralesById(idUsuario)
        idEmprendedor = data[0]["id"]
        emprendedor = data[0]
        session["emprendedor"] = emprendedor
        if request.method == "GET":
            # Datillos
            dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                idEmprendedor
            )
            data2 = logic.getNotification(idEmprendedor)
            return render_template(
                "emprendedorProfile.html",
                data=data,
                dataEmprendimiento=dataEmprendimiento,
                data2=data2,
                nombre=emprendedor["nombre"],
                email=emprendedor["email"],
                pais=emprendedor["pais"],
                ciudad=emprendedor["ciudad"],
                telefono=emprendedor["telefono"],
                biografia=emprendedor["biografia"],
            )

        elif request.method == "POST":
            verdadero = False
            verdaderoEmprendimiento = False
            formId = int(request.form["formId"])
            data2 = logic.getNotification(idEmprendedor)
            # Modificar informacion personal
            if formId == 1:
                id = idUsuario
                emprendedor = session["emprendedor"]
                nombre = emprendedor["nombre"]
                email = emprendedor["email"]
                telefono = emprendedor["telefono"]
                pais = emprendedor["pais"]
                ciudad = emprendedor["ciudad"]
                biografia = emprendedor["biografia"]

                verdadero = True

                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )
                data = logic.getDatosGeneralesById(id)
                return render_template(
                    "emprendedorProfile.html",
                    id=id,
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    verdadero=verdadero,
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    pais=pais,
                    ciudad=ciudad,
                    biografia=biografia,
                )

            # Aplicar cambios en informacion general
            elif formId == 2:
                emprendedor = session["emprendedor"]
                data2 = logic.getNotification(idEmprendedor)
                nombre = request.form["nombre"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                pais = request.form["pais"]
                ciudad = request.form["ciudad"]
                biografia = request.form["biografia"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename

                if foto.filename == "":
                    logic.updateEmprendedorbyIdUsuario(
                        idUsuario, nombre, email, telefono, pais, ciudad, biografia
                    )
                else:
                    binary_foto = foto.read()
                    logic.updateEmprendedorbyIdUsuarioWithPhoto(
                        idUsuario,
                        nombre,
                        email,
                        telefono,
                        pais,
                        ciudad,
                        biografia,
                        binary_foto,
                    )
                data = logic.getDatosGeneralesById(idUsuario)
                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )

                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    nombre=emprendedor["nombre"],
                    email=emprendedor["email"],
                    pais=emprendedor["pais"],
                    ciudad=emprendedor["ciudad"],
                    telefono=emprendedor["telefono"],
                    biografia=emprendedor["biografia"],
                )

            # Crear nuevo emprendimiento
            elif formId == 3:
                verdaderoEmprendimiento = True
                emprendedor = session["emprendedor"]
                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )
                data = logic.getDatosGeneralesById(idUsuario)
                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    verdaderoEmprendimiento=verdaderoEmprendimiento,
                    nombre=emprendedor["nombre"],
                    email=emprendedor["email"],
                    pais=emprendedor["pais"],
                    ciudad=emprendedor["ciudad"],
                    telefono=emprendedor["telefono"],
                    biografia=emprendedor["biografia"],
                )

            # Insertar nuevo emprendimiento
            elif formId == 4:
                data2 = logic.getNotification(idEmprendedor)
                id_emprendedor = idEmprendedor
                estado = request.form["estado"]
                descripcion = request.form["descripcion"]
                historia = request.form["historia"]
                eslogan = request.form["eslogan"]
                inversion_inicial = request.form["inversion_inicial"]
                fecha_fundacion = request.form["fecha_fundacion"]
                venta_año_anterior = request.form["venta_año_anterior"]
                nombre = request.form["nombre"]
                foto = request.files["fileToUpload"]
                nombre_foto = foto.filename
                video = request.form["video"]
                email = request.form["email"]
                telefono = request.form["telefono"]
                facebook = request.form["facebook"]
                instagram = request.form["instagram"]
                youtube = request.form["youtube"]
                emprendedor = session["emprendedor"]

                if foto.filename == "":
                    nombre_foto = "default.png"

                    logicEmprendimiento.insertNewEmprendimientoWithoutPhoto(
                        estado,
                        descripcion,
                        historia,
                        eslogan,
                        inversion_inicial,
                        fecha_fundacion,
                        venta_año_anterior,
                        id_emprendedor,
                        nombre,
                        nombre_foto,
                        video,
                        email,
                        telefono,
                        facebook,
                        instagram,
                        youtube,
                    )
                else:
                    binary_foto = foto.read()
                    logicEmprendimiento.insertNewEmprendimiento(
                        estado,
                        descripcion,
                        historia,
                        eslogan,
                        inversion_inicial,
                        fecha_fundacion,
                        venta_año_anterior,
                        id_emprendedor,
                        nombre,
                        binary_foto,
                        video,
                        email,
                        telefono,
                        facebook,
                        instagram,
                        youtube,
                    )

                data = logic.getDatosGeneralesById(idUsuario)
                emprendedor = session["emprendedor"]
                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    id_emprendedor
                )

                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    nombre=emprendedor["nombre"],
                    email=emprendedor["email"],
                    pais=emprendedor["pais"],
                    ciudad=emprendedor["ciudad"],
                    telefono=emprendedor["telefono"],
                    biografia=emprendedor["biografia"],
                )

            # Sale del emprendimiento by IdEmprendimiento
            elif formId == 5:
                data2 = logic.getNotification(idEmprendedor)
                id_emprendimiento = int(request.form["id"])
                logicEmprendimiento.salirEmprendimiento(
                    idEmprendedor, id_emprendimiento
                )
                data = logic.getDatosGeneralesById(idUsuario)
                dataEmprendimiento = logicEmprendimiento.getAllEmprendimientosByIdEmprendendor(
                    idEmprendedor
                )
                return render_template(
                    "emprendedorProfile.html",
                    data=data,
                    data2=data2,
                    dataEmprendimiento=dataEmprendimiento,
                    nombre=emprendedor["nombre"],
                    email=emprendedor["email"],
                    pais=emprendedor["pais"],
                    ciudad=emprendedor["ciudad"],
                    telefono=emprendedor["telefono"],
                    biografia=emprendedor["biografia"],
                )

            # Va hacia el emprendimiento que se selecciona
            elif formId == 6:
                id = int(request.form["id"])
                emprendimiento = logicEmprendimiento.getEmprendimientoById(id)
                session["emprendimiento"] = emprendimiento.id
                return redirect("/emprendimientoInicio")
    except KeyError:
        return render_template(
            "logInForm.html", messageSS="Su sesión ha expirado, ingrese nuevamente"
        )
