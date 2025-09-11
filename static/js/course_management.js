document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Edit Course
    const editButtons = document.querySelectorAll('.edit-course');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.dataset.id;
            const courseName = this.dataset.name;
            const trainerName = this.dataset.trainer;
            const price = this.dataset.price;
            const duration = this.dataset.duration;

            // Fill the edit modal with course data
            document.getElementById('editCourseId').value = courseId;
            document.getElementById('editCourseName').value = courseName;
            document.getElementById('editTrainerName').value = trainerName;
            document.getElementById('editCoursePrice').value = price;
            
            // Handle multi-select duration checkboxes
            // First, uncheck all checkboxes
            document.querySelectorAll('input[name="edit_duration"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            
            // Then check the appropriate ones based on comma-separated values
            if (duration) {
                const durationValues = duration.split(',');
                durationValues.forEach(value => {
                    const checkbox = document.querySelector(`input[name="edit_duration"][value="${value.trim()}"]`);
                    if (checkbox) {
                        checkbox.checked = true;
                    }
                });
            }

            // Show the modal
            const editModal = new bootstrap.Modal(document.getElementById('editCourseModal'));
            editModal.show();
        });
    });

    // Delete Course
    const deleteButtons = document.querySelectorAll('.delete-course');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this course?')) {
                const courseId = this.dataset.id;
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
                idInput.name = 'course_id';
                idInput.value = courseId;

                form.appendChild(csrfInput);
                form.appendChild(actionInput);
                form.appendChild(idInput);
                document.body.appendChild(form);
                form.submit();
            }
        });
    });

    // Search functionality
    const courseSearch = document.getElementById('courseSearch');
    if (courseSearch) {
        courseSearch.addEventListener('keyup', function() {
            const searchValue = this.value.toLowerCase();
            const table = document.getElementById('courseTable');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                if (row.cells.length > 1) { // Skip empty state row
                    const nameCell = row.cells[0].textContent.toLowerCase();
                    const trainerCell = row.cells[1].textContent.toLowerCase();
                    
                    if (nameCell.includes(searchValue) || trainerCell.includes(searchValue)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            }
        });
    }
}); 