function deleteWorkout(workoutId) {
    console.log("Delete button clicked, Workout ID:", workoutId); // Debugging
    if (confirm("Are you sure you want to delete this workout?")) {
        fetch(`/schedule/workout/delete/${workoutId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Delete response:", data); // Debugging
            if (data.status === 'success') {
                alert(data.message);
                location.reload(); // Reload the calendar
            } else {
                alert(data.message || 'An error occurred.');
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Ensure the Save button is functional
    const saveEditWorkoutBtn = document.getElementById('saveEditWorkoutBtn');
    if (saveEditWorkoutBtn) {
        saveEditWorkoutBtn.addEventListener('click', function () {
            const form = document.getElementById('editWorkoutForm');
            const workoutId = form.dataset.workoutId; // Get workout ID from data attribute
            const formData = new FormData(form);

            fetch(`/schedule/workout/edit/${workoutId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert(data.message);
                        location.reload(); // Reload the calendar
                    } else {
                        alert('Error: ' + JSON.stringify(data.errors));
                    }
                })
                .catch(error => {
                    console.error('Error submitting form:', error);
                });
        });
    }
});

function editWorkout(workoutId) {
    fetch(`/schedule/workout/edit/${workoutId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Inject form into the modal
                document.getElementById('editWorkoutBody').innerHTML = data.form;

                // Set the workout ID on the form
                const form = document.getElementById('editWorkoutForm');
                form.setAttribute('data-workout-id', workoutId);

                // Show the modal
                const editWorkoutModal = new bootstrap.Modal(document.getElementById('editWorkoutModal'));
                editWorkoutModal.show();
            } else {
                alert(data.message || 'An error occurred.');
            }
        })
        .catch(error => {
            console.error('Error fetching workout data:', error);
        });
}

// Handle form submission for edit
function submitEditForm(event) {
    event.preventDefault();
    const form = event.target;
    console.log("Edit form submitted:", form);

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Submit form response:", data);
        if (data.status === 'success') {
            alert(data.message);
            location.reload(); // Reload the calendar
        } else {
            alert('Error: ' + JSON.stringify(data.errors));
        }
    });
}
