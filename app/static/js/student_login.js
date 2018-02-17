$("#student_login_button").click(
	function(){
	var email = $("#student_login_email").val();		
	callstudent_login_function();

	
			}
	
	
	
	);


var callstudent_login_function=function()
			{
	

		var formx = $('form[name=frm1]');	
			 $.ajax({
                url : 'http://127.0.0.1:8080/student/login',
                method:"POST",
		dataType : 'json',
                data :  formx.serialize(),
                success : function(responce){
                alert("you are logged in");
		alert(responce.name);
				},
                error : function(message){
                alert("please fill valid details");
		console.log(message);	
				},
                }
        );


			}


