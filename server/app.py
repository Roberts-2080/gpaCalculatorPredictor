from flask import Flask, request, jsonify
from util.db_util import get_db_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/rank/v1/list', methods=['POST'])
def rank_list():
    """
    排名列表
    :return:
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from score order by avg_score desc")
    res = cursor.fetchall()

    cursor.close()
    connection.close()
    response = {
        "code": 0,
        "data": res,
        "msg": ""
    }
    # 返回JSON响应
    return jsonify(response)


@app.route('/api/rank/v1/add', methods=['POST'])
def add_rank():
    """
    添加排名
    :return:
    """
    response = {
        "code": 0,
        "data": 0.0,
        "msg": ""
    }
    body = request.get_json()
    username = body.get("username")
    semester_children = body.get("semester_children")
    if not username:
        response = {
            "code": 500,
            "data": None,
            "msg": "用户名不能为空"
        }
        return jsonify(response)
    num = 0
    all_score = 0

    for item in semester_children:
        if not item.get("semester_title"):
            response = {
                "code": 500,
                "data": None,
                "msg": "学期名称不能为空"
            }
            return jsonify(response)

        for i in item.get("course_children"):
            course_title = i.get("course_title")
            score = i.get("score")
            if not course_title or not score:
                response = {
                    "code": 500,
                    "data": None,
                    "msg": "课程名或分数不能为空"
                }
                return jsonify(response)
            score = int(score)

            if score > 100:
                response["code"] = 500
                response["msg"] = "分数不能大于100"
                return jsonify(response)
            all_score += score
            num += 1

    avg_score = all_score / num
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"insert into score(username, avg_score) values('{username}', {round(avg_score, 2)})")
        connection.commit()

        cursor.execute("select * from score order by avg_score desc")
        res = cursor.fetchall()
        all_rank = 0
        for item in res:
            all_rank += 1
            if item.get("username") == username:
                rank = round((len(res) - all_rank + 1) / len(res) * 100, 2)
                response["data"] = rank

        cursor.close()
        connection.close()
    except Exception as e:
        response["msg"] = str(e)
        response["code"] = 500

    return jsonify(response)


@app.route('/api/rank/v1/del', methods=['POST'])
def del_rank():
    """
    删除排名
    :return:
    """
    body = request.get_json()
    user_id = body.get("id")
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"delete from score where id={user_id}")
    connection.commit()
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    return jsonify(response)


@app.route('/api/semester/v1/list', methods=['POST'])
def semester_list():
    """
    学期列表
    :return:
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from semester")
    res = cursor.fetchall()
    response = {
        "code": 0,
        "data": res,
        "msg": ""
    }
    return jsonify(response)


@app.route('/api/course/v1/add', methods=['POST'])
def add_course():
    """
    添加课程
    :return:
    """
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    body = request.get_json()
    title = body.get("title")
    pass_line = body.get("pass_line")
    if not title or not pass_line:
        response = {
            "code": 500,
            "data": None,
            "msg": "课程或及格线不能为空"
        }
        return jsonify(response)
    pass_line = int(pass_line)
    if pass_line > 100:
        response["code"] = 500
        response["msg"] = "及格线不能大于100"
        return jsonify(response)

    semester_id = body.get("semester_id")
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            f"insert into course(title, pass_line, semester_id) values('{title}', {pass_line}, {semester_id})")
        connection.commit()

    except Exception as e:
        response["msg"] = str(e)
        response["code"] = 500

    return jsonify(response)


@app.route('/api/course/v1/update', methods=['POST'])
def update_course():
    """
    更新课程
    :return:
    """
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    body = request.get_json()
    title = body.get("title")
    course_id = body.get("id")
    pass_line = body.get("pass_line")
    if not title or not pass_line:
        response = {
            "code": 500,
            "data": None,
            "msg": "课程或及格线不能为空"
        }
        return jsonify(response)
    pass_line = int(pass_line)
    if pass_line > 100:
        response["code"] = 500
        response["msg"] = "及格线不能大于100"
        return jsonify(response)
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"update course set title='{title}',pass_line={pass_line} where id={course_id}")
        connection.commit()

    except Exception as e:
        response["msg"] = str(e)
        response["code"] = 500

    return jsonify(response)


@app.route('/api/course/v1/del', methods=['POST'])
def del_course():
    """
    删除课程
    :return:
    """
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    body = request.get_json()
    course_id = body.get("id")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"delete from course where id={course_id}")
        connection.commit()

    except Exception as e:
        response["msg"] = str(e)
        response["code"] = 500

    return jsonify(response)


@app.route('/api/course/v1/list', methods=['POST'])
def course_list():
    """
    课程列表
    :return:
    """
    body = request.get_json()
    semester_id = body.get("id")
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"select * from course where semester_id={semester_id}")
    course_res = cursor.fetchall()
    for course in course_res:
        cursor.execute(f"select count(*) c from course_module where course_id={course['id']}")
        module_res = cursor.fetchone()
        course["assessment_count"] = module_res.get("c")
    response = {
        "code": 0,
        "data": course_res,
        "msg": ""
    }
    return jsonify(response)


@app.route('/api/module/v1/list', methods=['POST'])
def module_list():
    """
    模块列表
    :return:
    """
    body = request.get_json()
    course_id = body.get("course_id")
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"select * from course_module where course_id={course_id}")
    module_res = cursor.fetchall()

    response = {
        "code": 0,
        "data": module_res,
        "msg": ""
    }
    return jsonify(response)


@app.route('/api/module/v1/del', methods=['POST'])
def del_module():
    """
    删除模块
    :return:
    """
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    body = request.get_json()
    module_id = body.get("id")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"delete from course_module where id={module_id}")
        connection.commit()

    except Exception as e:
        response["msg"] = str(e)
        response["code"] = 500

    return jsonify(response)


@app.route('/api/module/v1/update', methods=['POST'])
def update_module():
    """
    更新模块
    :return:
    """
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    body = request.get_json()
    title = body.get("title")
    module_id = body.get("id")
    course_id = body.get("course_id")
    grade_percentage = body.get("grade_percentage")
    if not title or not grade_percentage:
        response = {
            "code": 500,
            "data": None,
            "msg": "测评标题或成绩占比不能为空"
        }
        return jsonify(response)
    grade_percentage = int(grade_percentage)
    if grade_percentage > 99:
        response["code"] = 500
        response["msg"] = "总成绩占比不能大于99"
        return jsonify(response)

    test_score = body.get("test_score")
    if test_score:
        test_score = int(test_score)
        if test_score > 100:
            response["code"] = 500
            response["msg"] = "测试满分不能大于100"
            return jsonify(response)

    current_score = body.get("current_score")
    if current_score:
        current_score = int(current_score)
        if current_score > 100:
            response["code"] = 500
            response["msg"] = "已得分数不能大于100"
            return jsonify(response)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(f"select * from course_module where course_id={course_id} and id!={module_id}")
        module_res = cursor.fetchall()
        all_grade_percentage = grade_percentage
        for m in module_res:
            if not m.get("grade_percentage"):
                continue
            all_grade_percentage += m.get("grade_percentage")
            if all_grade_percentage > 99:
                response["code"] = 500
                response["msg"] = "总成绩占比不能大于99"
                return jsonify(response)
        test_score = test_score if test_score else 'null'
        current_score = current_score if current_score else 'null'
        cursor.execute(f"""
        update course_module 
            set title='{title}',grade_percentage={grade_percentage},test_score={test_score},current_score={current_score}
        where 
            id={module_id} and course_id={course_id}
        """)
        connection.commit()

    except Exception as e:
        response["msg"] = str(e)
        response["code"] = 500

    return jsonify(response)


@app.route('/api/module/v1/add', methods=['POST'])
def add_module():
    """
    添加模块
    :return:
    """
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    body = request.get_json()
    title = body.get("title")
    course_id = body.get("course_id")
    grade_percentage = body.get("grade_percentage")
    if not title or not grade_percentage:
        response = {
            "code": 500,
            "data": None,
            "msg": "测评标题或成绩占比不能为空"
        }
        return jsonify(response)
    grade_percentage = int(grade_percentage)
    if grade_percentage > 99:
        response["code"] = 500
        response["msg"] = "总成绩占比不能大于99"
        return jsonify(response)

    test_score = body.get("test_score")
    if test_score:
        test_score = int(test_score)
        if test_score > 100:
            response["code"] = 500
            response["msg"] = "测试满分不能大于100"
            return jsonify(response)

    current_score = body.get("current_score")
    if current_score:
        current_score = int(current_score)
        if current_score > 100:
            response["code"] = 500
            response["msg"] = "已得分数不能大于100"
            return jsonify(response)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(f"select * from course_module where course_id={course_id}")
        module_res = cursor.fetchall()
        all_grade_percentage = grade_percentage
        for m in module_res:
            if not m.get("grade_percentage"):
                continue
            all_grade_percentage += m.get("grade_percentage")
            if all_grade_percentage > 99:
                response["code"] = 500
                response["msg"] = "总成绩占比不能大于99"
                return jsonify(response)

        cursor.execute(f"""
        insert into 
            course_module(title, grade_percentage, test_score, current_score, course_id)
        values('{title}', {grade_percentage}, {test_score}, {current_score}, {course_id})        
        """)
        connection.commit()

    except Exception as e:
        response["msg"] = str(e)
        response["code"] = 500

    return jsonify(response)


@app.route('/api/score/v1/predict', methods=['POST'])
def score_predict():
    response = {
        "code": 0,
        "data": None,
        "msg": ""
    }
    body = request.get_json()
    course_id = body.get("course_id")
    # 预期线
    prediction_line = body.get("prediction_line")
    # 测试占比
    test_percentage = body.get("test_percentage")
    if not prediction_line or not test_percentage:
        response = {
            "code": 500,
            "data": None,
            "msg": "预期线或最终测试占比不能为空"
        }
        return jsonify(response)
    test_percentage = int(test_percentage)
    prediction_line = int(prediction_line)
    if prediction_line > 100 or test_percentage > 100:
        response = {
            "code": 500,
            "data": None,
            "msg": "预期线或最终测试占比不能大于100"
        }
        return jsonify(response)
    if prediction_line < 60:
        response = {
            "code": 500,
            "data": None,
            "msg": "预期线不能小于60"
        }
        return jsonify(response)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"select * from course_module where course_id={course_id}")
    module_res = cursor.fetchall()
    all_current_score = 0
    all_grade_percentage = test_percentage
    for m in module_res:
        grade_percentage = m.get("grade_percentage")
        current_score = m.get("current_score")
        if not grade_percentage or not current_score:
            response = {
                "code": 500,
                "data": None,
                "msg": "现有模块成绩占比或已得分数不能为空"
            }
            return jsonify(response)
        all_grade_percentage += grade_percentage
        if all_grade_percentage > 100:
            response = {
                "code": 500,
                "data": None,
                "msg": "总成绩占比不能大于100"
            }
            return jsonify(response)
        all_current_score += grade_percentage / 100 * current_score

    if all_grade_percentage != 100:
        response = {
            "code": 500,
            "data": None,
            "msg": f"总成绩占比: {all_grade_percentage}, 必须等于100, 请调整"
        }
        return jsonify(response)

    x = (prediction_line - all_current_score) / (test_percentage / 100) if (prediction_line - all_current_score) / (
            test_percentage / 100) > 0 else 0
    if x > 100:
        response = {
            "code": 500,
            "data": None,
            "msg": f"预测成绩: {x}, 分数不能大于100, 预测失败"
        }
        return jsonify(response)

    response = {
        "code": 0,
        "data": round(x, 2),
        "msg": ""
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
