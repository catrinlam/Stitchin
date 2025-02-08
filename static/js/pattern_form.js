console.log('pattern_form.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    function toggleSizeFields(row) {
        const typeField = row.querySelector('[name*="type"]');
        const hookSizeField = row.querySelector('[name*="hook_size"]').closest('.form-group');
        const needleSizeField = row.querySelector('[name*="needle_size"]').closest('.form-group');

        function updateVisibility() {
            if (typeField.value === '0') {
                hookSizeField.style.display = 'block';
                needleSizeField.style.display = 'none';
            } else if (typeField.value === '1') {
                hookSizeField.style.display = 'none';
                needleSizeField.style.display = 'block';
            } else {
                hookSizeField.style.display = 'none';
                needleSizeField.style.display = 'none';
            }
        }

        updateVisibility();
        typeField.addEventListener('change', updateVisibility);
    }

    document.querySelectorAll('#hooks-needles-formset .form-row').forEach(toggleSizeFields);

    const formsetContainer = document.getElementById('hooks-needles-formset');
    const addFormsetButton = document.getElementById('add-formset');
    const totalForms = document.getElementById('id_pattern_hooks_needles-TOTAL_FORMS');
    let formCount = totalForms.value;

    addFormsetButton.addEventListener('click', function() {
        let currentFormCount = formsetContainer.children.length;
        const newForm = formsetContainer.children[0].cloneNode(true);
        const formRegex = RegExp(`pattern_hooks_needles-(\\d){1}-`, 'g');

        console.log('form count', formCount);
        formCount++;

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `pattern_hooks_needles-${currentFormCount}-`);
        formsetContainer.appendChild(newForm);
        totalForms.setAttribute('value', formCount + 1);
        currentFormCount++;

        toggleSizeFields(newForm);

        // Add a delete button to the new form
        const deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.className = 'btn btn-danger remove-form mt-2';
        deleteButton.textContent = 'Remove';
        deleteButton.addEventListener('click', function() {
            newForm.remove();
            formCount--;
            totalForms.setAttribute('value', formCount);
        });
        newForm.appendChild(deleteButton);

        formsetContainer.appendChild(newForm);
        totalForms.setAttribute('value', formCount);
    });

    // Add delete functionality to existing forms
    document.querySelectorAll('.remove-form').forEach(button => {
        button.addEventListener('click', function() {
            button.closest('.form-row').remove();
            formCount--;
            totalForms.setAttribute('value', formCount);
        });
    });
});