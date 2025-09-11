document.addEventListener('DOMContentLoaded', function() {
    // Edit CSR
    const editButtons = document.querySelectorAll('.edit-csr');
    const editModal = document.getElementById('editCSRModal');
    const editForm = editModal.querySelector('form');
    const editCSRId = document.getElementById('editCSRId');
    const editFullName = document.getElementById('editFullName');
    const editUsername = document.getElementById('editUsername');
    const editIsActive = document.getElementById('editIsActive');
    const editLeadRole = document.getElementById('editLeadRole');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const csrId = this.dataset.id;
            const csrName = this.dataset.name;
            const csrUsername = this.dataset.username;
            const isActive = this.dataset.active === 'true';
            const isLead = this.dataset.lead === 'true';

            editCSRId.value = csrId;
            editFullName.value = csrName;
            editUsername.value = csrUsername;
            editIsActive.checked = isActive;
            editLeadRole.checked = isLead;

            const editCSRModal = new bootstrap.Modal(editModal);
            editCSRModal.show();
        });
    });

    // Delete CSR
    const deleteButtons = document.querySelectorAll('.delete-csr');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this CSR?')) {
                const csrId = this.dataset.id;
                const form = document.createElement('form');
                form.method = 'POST';
                form.style.display = 'none';

                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;

                const actionInput = document.createElement('input');
                actionInput.type = 'hidden';
                actionInput.name = 'action';
                actionInput.value = 'delete';

                const idInput = document.createElement('input');
                idInput.type = 'hidden';
                idInput.name = 'csr_id';
                idInput.value = csrId;

                form.appendChild(csrfInput);
                form.appendChild(actionInput);
                form.appendChild(idInput);
                document.body.appendChild(form);
                form.submit();
            }
        });
    });

    // Password validation for add CSR form
    const addForm = document.getElementById('addCSRForm');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');

    addForm.addEventListener('submit', function(e) {
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            alert('Passwords do not match!');
        }
    });
}); 