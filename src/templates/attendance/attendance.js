<script>
    $(document).ready(function () {

       
        $("#fetch_student").click(function () {
            var subject = $("#subject").val()
            var class_id = $("#class").val()
            $("#student_data").html(null)
if (subject.length  == 0){
    alert("Please select session and subject");
    return false;
}
            $.ajax({
                url: "{% url 'attendance:get-students' %}",
                type: 'POST',
                data: {
                    subject: subject,
                    class_id: class_id,
                }
            }).done(function (response) {
                var json_data = JSON.parse(response)
                if (json_data.length < 1) {
                    alert("No data to display")
                } else {
                    var div_data = "<hr/><div class='form-group'></div><div class='form-group'> <label>Attendance Date</label><input type='date' class='form-control' name='attendance_date' id='attendance_date' ><div class='row'>"

                    for (key in json_data) {
                        div_data += "<div class='col-lg-3'><div class='form-check custom-control custom-checkbox'><input type='checkbox' class='custom-control-input' checked='checked' name='student_data[]' value=" + json_data[key]['id'] + " id='checkbox" + json_data[key]['id'] + "' /> <label for='checkbox" + json_data[key]['id'] + "' class='custom-control-label'>" + json_data[key]['name'] + "</label></div> </div>"
                    }
                    div_data += "</div></div>"
                    div_data += "<div class='form-group'><button id='save_attendance' class='btn btn-success' type='button'>Save Attendance</button></div>"
                    $("#student_data").html(div_data)
                }
            }).fail(function (response) {
                alert("Error in fetching students")
            })


            $(document).on('click', '#save_attendance', function () {
                $(this).attr("disabled","disabled")
                $(this).text("Saving Attendance Data...")
                var student_data = $("input[name='student_data[]']").map(function () {
                    if ($(this).is(":checked")){
                    return {'id':$(this).val(), 'status': 1};
    
                    }
                    return {'id':$(this).val(), 'status': 0};
    
                }).get()
                var attendance_date = $('#attendance_date').val()
                if (attendance_date.length < 10){
                    alert("Select date")
                    return false;
                }
                student_data = JSON.stringify(student_data)
                $.ajax({
                    url: "{% url 'attendance:save_attendance' %}",
                    type: 'POST',
                    data: {
                        date: attendance_date,
                        student_ids: student_data,
                        subject: subject,
                        session: session
            
                    }
                }).done(function (response) {
                    if (response == 'OK'){
                        alert("Saved")
                    }else{
                        alert("Error. Please try again")
                    }
                    location.reload()
                    
                }).fail(function (response) {
                    alert("Error in saving attendance")
                })
    
            })


        })
    })
</script>