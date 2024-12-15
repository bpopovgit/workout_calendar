// Mark Workout as Completed
function markCompleted(workoutId) {
    console.log("Mark Completed clicked, Workout ID:", workoutId); // Debugging
    fetch(`/schedule/mark-completed/${workoutId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log("Mark Completed response:", data); // Debugging
        if (data.status === 'success') {
            alert(data.message);
            location.reload(); // Reload the calendar
        } else {
            alert(data.message || 'An error occurred.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Delete Workout
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
        })
        .catch(error => console.error('Error:', error));
    }
}

// Edit Workout
function editWorkout(workoutId) {
    console.log("Edit button clicked, Workout ID:", workoutId); // Debugging
    fetch(`/schedule/workout/edit/${workoutId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log("Edit response:", data); // Debugging
        if (data.status === 'success') {
            document.getElementById('editWorkoutBody').innerHTML = data.form;
            const modal = new bootstrap.Modal(document.getElementById('editWorkoutModal'));
            modal.show();

            document.getElementById('saveEditWorkoutBtn').onclick = function () {
                saveEditWorkout(workoutId);
            };
        } else {
            alert('Failed to load form: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Save Edited Workout
function saveEditWorkout(workoutId) {
    console.log("Save Edit button clicked, Workout ID:", workoutId); // Debugging
    const formData = new FormData(document.querySelector('#editWorkoutModal form'));
    fetch(`/schedule/workout/edit/${workoutId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log("Save Edit response:", data); // Debugging
        if (data.status === 'success') {
            alert(data.message);
            location.reload(); // Reload the calendar
        } else {
            alert('Error saving workout: ' + JSON.stringify(data.errors));
        }
    })
    .catch(error => console.error('Error:', error));
}

// Adjust Calendar Cell Heights
function adjustCalendarCellHeights() {
    const cells = document.querySelectorAll('.calendar-table td');
    let maxHeight = 0;

    // Determine the maximum height of all cells
    cells.forEach(cell => {
        const cellHeight = cell.getBoundingClientRect().height;
        if (cellHeight > maxHeight) maxHeight = cellHeight;
    });

    // Apply the maximum height to all cells
    cells.forEach(cell => {
        cell.style.height = `${maxHeight}px`;
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed. Attaching event listeners."); // Debugging

    // Attach event listeners to buttons
    document.querySelectorAll('.mark-completed-btn').forEach(button => {
        button.addEventListener('click', () => {
            const workoutId = button.getAttribute('data-workout-id');
            markCompleted(workoutId);
        });
    });

    document.querySelectorAll('.edit-workout-btn').forEach(button => {
        button.addEventListener('click', () => {
            const workoutId = button.getAttribute('data-workout-id');
            editWorkout(workoutId);
        });
    });

    document.querySelectorAll('.delete-workout-btn').forEach(button => {
        button.addEventListener('click', () => {
            const workoutId = button.getAttribute('data-workout-id');
            deleteWorkout(workoutId);
        });
    });

    // Adjust calendar cell heights
    adjustCalendarCellHeights();
});
