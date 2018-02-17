$("#faculty_register_button").click(
        function(){
        var email = $("#faculty_register_email").val();
        var name = $("#faculty_register_name").val();
        var password = $("#faculty_register_password").val();
        var course_id = $("#faculty_register_course_id").val();
	var course_name = $("#faculty_register_course_name").val();
	var course_description = $("#faculty_register_course_description").val();

        if(password.length <= 7)
        {
	$("#faculty_register_error").text("please enter atleast 8 charecters for password");
	}
	
	if(name.length === 0 || (course_name).length === 0)
	{
	$("#faculty_register_error").text("please enter valid details");
	
		}
       if(course_id.length >= 7)
	{
	$("#faculty_register_error").text("please enter valid course-id");
	
	}
 	
        callfaculty_register_function(email);

                        }



        );


var callfaculty_register_function=function(email)
{	

	console.log("enter");
	$.ajax({
	url : 'http://127.0.0.1:8080/faculty/register',
	method : "post",
	data : $('form').serialize(),
	dataType : 'json',
	success : function(){
		
			alert("True");		
		},
	error: function(){
			alert("false");

			},	


	});





};


