// =====================================
// LOADER HTMX
// =====================================

document.body.addEventListener(
    'htmx:beforeRequest',
    function () {

        const loader = document.getElementById('loader');

        if (loader) {
            loader.style.display = 'flex';
        }

        const contenido = document.getElementById('contenido');

        if (contenido) {
            contenido.classList.add('contenido-saliendo');
        }

    }
);

document.body.addEventListener(
    'htmx:afterSwap',
    function () {

        const contenido = document.getElementById('contenido');

        if (contenido) {

            contenido.classList.remove('contenido-saliendo');

            contenido.classList.add('contenido-entrando');

            setTimeout(
                function () {
                    contenido.classList.remove('contenido-entrando');
                },
                250
            );

        }

    }
);

document.body.addEventListener(
    'htmx:afterRequest',
    function () {

        const loader = document.getElementById('loader');

        if (loader) {
            loader.style.display = 'none';
        }

    }
);

// =====================================
// CERRAR MODAL AL HACER CLICK FUERA
// =====================================

document.addEventListener(
    'click',
    function (event) {

        if (
            event.target.classList.contains(
                'modal-overlay'
            )
        ) {

            cerrarModal();

        }

    }
);

// =====================================
// REFRESCAR EMPLEADOS
// =====================================

document.body.addEventListener(
    'empleadoGuardado',
    function () {

        cerrarModal();

        htmx.ajax(
            'GET',
            '/empleados/',
            {
                target: '#contenido',
                swap: 'innerHTML'
            }
        );

    }
);

// =====================================
// REFRESCAR PLANILLAS
// =====================================

document.body.addEventListener(
    'planillaGenerada',
    function () {

        htmx.ajax(
            'GET',
            '/planillas/',
            {
                target: '#contenido',
                swap: 'innerHTML'
            }
        );

    }
);

// =====================================
// CERRAR MODAL
// =====================================

function cerrarModal() {

    const modalContainer =
        document.getElementById(
            'modal-container'
        );

    if (modalContainer) {
        modalContainer.innerHTML = '';
    }

    document
        .querySelectorAll(
            '.modal-backdrop'
        )
        .forEach(
            backdrop => backdrop.remove()
        );

    document.body.classList.remove(
        'modal-open'
    );

    document.body.style.removeProperty(
        'overflow'
    );

    document.body.style.removeProperty(
        'padding-right'
    );

}

// =====================================
// ABRIR MODAL BOOTSTRAP SI EXISTE
// =====================================

document.body.addEventListener(
    'htmx:afterSwap',
    function () {

        const modalElement =
            document.querySelector(
                '#modal-container .modal'
            );

        if (modalElement) {

            try {

                const modal =
                    new bootstrap.Modal(
                        modalElement
                    );

                modal.show();

            } catch (error) {

                console.log(
                    'Bootstrap Modal:',
                    error
                );

            }

        }

    }
);