from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class TrainCoach:
    def __init__(self):
        # Initialize the train coach with 80 total seats, arranged in 10 rows with varying seat numbers per row.
        self.total_seats = 80
        self.rows = 10
        self.seats_per_row = [7] * (self.rows - 1) + [3]
        self.seats = [['O'] * row for row in self.seats_per_row]

    def reserve_seats(self, num_seats):
        # Method to reserve a specified number of seats in the train coach.
        # Returns a list of reserved seat numbers.
        seats_reserved = []
        for row_num, row in enumerate(self.seats):
            available_seats = ''.join(row).count('O')  # Count available seats in the row.
            if available_seats >= num_seats:  # If there are enough available seats in the row.
                start_seat = row.index('O')  # Find the index of the first available seat.
                end_seat = start_seat + num_seats  # Calculate the index of the last seat to be reserved.
                # Generate a list of reserved seat numbers and mark those seats as reserved ('X').
                reserved_seats = [f"{row_num}-{seat}" for seat in range(start_seat + 1, end_seat + 1)]
                self.seats[row_num][start_seat:end_seat] = ['X'] * num_seats
                seats_reserved.extend(reserved_seats)
                break  # Exit the loop after reserving seats in the first eligible row.
        return seats_reserved

train_coach = TrainCoach()

@app.route('/')
def index():
    # Render the index.html template.
    return render_template('index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    # Handle reservation requests.
    num_seats = int(request.form['num_seats'])  # Extract the number of seats requested from the request.
    reserved_seats = train_coach.reserve_seats(num_seats)  # Reserve seats in the train coach.
    return jsonify({'reserved_seats': reserved_seats})  # Return the reserved seat numbers in JSON format.

if __name__ == '__main__':
    # Run the Flask application in debug mode.
    app.run(debug=True)
