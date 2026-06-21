// =====================================
// LOADER HTMX
// =====================================

document.body.addEventListener(
    'htmx:beforeRequest',
    function () {

        const loader =
            document.getElementById(
                'loader'
            );

        if (loader) {

            loader.style.display =
                'flex';

        }

    }
);

document.body.addEventListener(
    'htmx:afterRequest',
    function () {

        const loader =
            document.getElementById(
                'loader'
            );

        if (loader) {

            loader.style.display =
                'none';

        }

    }
);

// =====================================
// EMPLEADO GUARDADO
// =====================================

document.body.addEventListener(
    'empleadoGuardado',
    function () {

        cerrarModal();

    }
);

// =====================================
// PLANILLA GENERADA
// =====================================

document.body.addEventListener(
    'planillaGenerada',
    function () {

        cerrarModal();

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
// ABRIR MODAL BOOTSTRAP
// =====================================

document.body.addEventListener(
    'htmx:afterSwap',
    function () {

        const modalElement =
            document.querySelector(
                '.modal'
            );

        if (modalElement) {

            try {

                const modal =
                    new bootstrap.Modal(
                        modalElement
                    );

                modal.show();

            }
            catch (error) {

                console.log(
                    error
                );

            }

        }

    }
);