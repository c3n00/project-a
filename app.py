from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)
SEATS_FILE = os.path.join(os.path.dirname(__file__), 'seats.json')
TOTAL_SEATS = 47

# 좌석 정보 파일에서 불러오기
def load_seats():
    if not os.path.exists(SEATS_FILE):
        return {}
    with open(SEATS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}

# 좌석 정보 파일에 저장하기
def save_seats(seats):
    with open(SEATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(seats, f, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

# 좌석 현황 조회 API
@app.route('/api/seats', methods=['GET'])
def get_seats():
    seats = load_seats()
    return jsonify(seats)

# 좌석 예약 API
@app.route('/api/reserve', methods=['POST'])
def reserve_seat():
    data = request.json
    if not data:
        return jsonify({'success': False, 'msg': '필수 정보 누락'}), 400
    seat_num = str(data.get('seatNum'))
    student_id = data.get('id')
    student_name = data.get('name')
    end_period = data.get('endPeriod')
    if not (seat_num and student_id and student_name and end_period):
        return jsonify({'success': False, 'msg': '필수 정보 누락'}), 400
    seats = load_seats()
    # 이미 해당 학번으로 예약된 좌석이 있는지 확인
    for s in seats.values():
        if s['id'] == student_id:
            return jsonify({'success': False, 'msg': '이미 예약한 좌석이 있습니다.'}), 400
    # 이미 예약된 좌석인지 확인
    if seat_num in seats:
        return jsonify({'success': False, 'msg': '이미 예약된 좌석입니다.'}), 400
    # 예약 처리
    seats[seat_num] = {'id': student_id, 'name': student_name, 'endPeriod': end_period}
    save_seats(seats)
    return jsonify({'success': True})

# 좌석 초기화(관리자용, 필요시)
@app.route('/api/reset', methods=['POST'])
def reset_seats():
    save_seats({})
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 