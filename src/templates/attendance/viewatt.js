
    $(document).ready(function () {
        $("#fetch_attendance").click(function(){
            var subject = $("#subject").val()
            var session = $("#session").val()
            if (session.length < 1 || subject.length < 1){
                $("#error_attendance").html("Kindly Choose Both Subject and Session")
                $("#attendance_block").hide()
                $("#error_attendance").show()
                return false
            }
            $.ajax({
                url: "{% url 'attendance:get_attendance' %}",
                type: 'POST',
                data:{
                    subject:subject,
                    session:session
                }
            
            }

            ).done(function(response){
                var json_data = JSON.parse(response)
                if (json_data.length > 0){

                    var html = "";
                    for (key in json_data){
                        html += "<option value='"+json_data[key]['id']+"'>"+json_data[key]['attendance_date']+"</option>"
                    }
                    $("#attendance_date").html(html)
                    $("#error_attendance").hide()
                    $("#error_attendance").html("")
                    $("#attendance_block").show()  
                    $("#fetch_student_block").show()
                }else{
                    $("#error_attendance").html("No Attendance Date Found For Specified Data")
                    $("#error_attendance").show()
                    $("#attendance_date").html("")
                    $("#attendance_block").hide()


                }
            }).fail(function(response){
                alert("Error While Fetching Data")
                $("#error_attendance").html("")
                $("#error_attendance").show()
                $("#attendance_block").hide()


            })
        })

        $("#fetch_student").click(function () {
            var attendance_date = $("#attendance_date").val()
            $("#student_data").html(null)
if (attendance_date.length  == 0){
    alert("Please Choose A Date");
    $("#save_attendance").hide()

    return false;
}
            $.ajax({
                url: "{% url 'get_student_attendance' %}",
                type: 'POST',
                data: {
                    attendance_date_id:attendance_date,
                }
            }).done(function (response) {
                var json_data = JSON.parse(response)
                if (json_data.length < 1) {
                    alert("No data to display")
            $("#save_attendance").hide()

                } else {
            $("#save_attendance").show()

                    var div_data = "<hr/><div class='form-group'></div><div class='form-group'> <label>Student Attendance</label><div class='row'>"

                    for (key in json_data) {
                        div_data += "<div class='col-lg-3'><div class='form-check custom-control custom-checkbox'><input type='checkbox' class='custom-control-input' " + (json_data[key]['status'] ? "checked='checked'" : "")+" name='student_data[]' value=" + json_data[key]['id'] + " id='checkbox" + json_data[key]['id'] + "' /> <label for='checkbox" + json_data[key]['id'] + "' class='custom-control-label'>" + json_data[key]['name']  + (json_data[key]['status'] ? " [Present] " : " [Absent] ")+"</label></div> </div>"
                    }
                    div_data += "</div></div>"
                    div_data += "<div class='form-group'><button id='save_attendance' class='btn btn-success' type='button'>Save Attendance</button></div>"
                    $("#student_data").html(div_data)
                }
            }).fail(function (response) {
                alert("Error in fetching students")
            })

        })
        $(document).on('click', '#save_attendance', function () {
            //$(this).attr("disabled","disabled")
            $(this).text("Updating Attendance Data...")
            var student_data = $("input[name='student_data[]']").map(function () {
                if ($(this).is(":checked")){
                return {'id':$(this).val(), 'status': 1};

                }
                return {'id':$(this).val(), 'status': 0};

            }).get()
      
            student_data = JSON.stringify(student_data)
            var attendance_date = $("#attendance_date").val()
            $.ajax({
                url: "{% url 'update_attendance' %}",
                type: 'POST',
                data: {
                    date: attendance_date,
                    student_ids: student_data,
                }
            }).done(function (response) {
                if (response == 'OK'){
                    alert("Updated")
                }else{
                    alert("Error. Please try again")
                }
                location.reload()
                
            }).fail(function (response) {
                alert("Error in saving attendance")
            })

        })
    })
