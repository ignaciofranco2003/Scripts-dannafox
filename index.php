<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menú de Opciones</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            padding: 20px;
        }
        .form-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            margin-top: 20px;
            padding: 10px;
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
        }
    </style>
</head>

<body>
    <div class="form-container">
        <h1>Menú de Opciones</h1>
        <form method="POST" action="">
            <label for="opcion">Selecciona una opción:</label>
            <select id="opcion" name="opcion" required>
                <option value="">-- Selecciona --</option>
                <option value="1">Crear y suministrar números a la base de datos</option>
                <option value="2">Generar archivos Access</option>
                <option value="3">Generar reporte de una campaña</option>
                <option value="4">Salir</option>
            </select>

            <div id="opcion1" style="display: none;">
                <label for="localidad">Nombre de la localidad:</label>
                <input type="text" id="localidad" name="localidad" placeholder="Ej: Ciudad" />

                <label for="cantidad">Cantidad de números a generar:</label>
                <input type="number" id="cantidad" name="cantidad" placeholder="Ej: 100" />
            </div>

            <div id="opcion3" style="display: none;">
                <label for="id_campania">ID de la campaña:</label>
                <input type="text" id="id_campania" name="id_campania" placeholder="Ej: 12345" />
            </div>

            <button type="submit">Ejecutar</button>
        </form>
        <?php
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $opcion = $_POST['opcion'];

            switch ($opcion) {
                case "1":
                    $localidad = $_POST['localidad'] ?? null;
                    $cantidad = $_POST['cantidad'] ?? null;

                    if ($localidad && $cantidad) {
                        // Llama a tu script de Python para ejecutar main()
                        $localidad = escapeshellarg($localidad); // Escapar la localidad para manejar espacios y caracteres especiales
                        $command = ".venv\\Scripts\\activate && python generar_numeros.py $localidad $cantidad";  // Usar comillas dobles
                        $output = shell_exec($command);
                        echo "<div class='message'>Opción 1 ejecutada: <br/> $output</div>";
                    } else {
                        echo "<div class='message' style='background-color: #f8d7da; color: #721c24;'>Complete todos los campos.</div>";
                    }
                    break;

                case "2":
                    // Lógica para opción 2
                    echo "<div class='message'>Opción 2 ejecutada: Generando datos...</div>";
                    break;

                case "3":
                    $id_campania = $_POST['id_campania'] ?? null;

                    if ($id_campania) {
                        // Llama a tu script de Python para ejecutar generate_campaign_report
                        $command = ".venv\\Scripts\\activate && python generate_campaign_report.py $id_campania";
                        $output = shell_exec($command);
                        echo "<div class='message'>Opción 3 ejecutada: <br/> $output </div>";
                    } else {
                        echo "<div class='message' style='background-color: #f8d7da; color: #721c24;'>Faltan datos para la opción 3.</div>";
                    }
                    break;

                case "4":
                    echo "<div class='message'>Saliendo del sistema. ¡Hasta luego!</div>";
                    break;

                default:
                    echo "<div class='message' style='background-color: #f8d7da; color: #721c24;'>Opción no válida.</div>";
                    break;
            }
        }
        ?>
    </div>

    <script>
        document.getElementById('opcion').addEventListener('change', function () {
            document.getElementById('opcion1').style.display = 'none';
            document.getElementById('opcion3').style.display = 'none';

            if (this.value === "1") {
                document.getElementById('opcion1').style.display = 'block';
            } else if (this.value === "3") {
                document.getElementById('opcion3').style.display = 'block';
            }
        });
    </script>
</body>
</html>
