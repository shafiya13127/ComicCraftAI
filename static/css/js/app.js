document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                "#comic-form"
            );

        const button =
            document.querySelector(
                "#submit-button"
            );

        if (!form || !button) {
            return;
        }

        form.addEventListener(
            "submit",
            () => {

                button.disabled = true;

                button.textContent =
                    "Creating your comic...";

            }
        );

    }
);