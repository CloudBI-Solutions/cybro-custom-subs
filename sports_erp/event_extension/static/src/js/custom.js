var u_name = []
var email = []
var phone = []
var dob = []
var med_info = []
var event_ticket_ids = []
function ticket(checked, id)
{
    var select_string = 'nb_register-' + id;
    console.log(select_string, "string")
    var select = document.getElementsByClassName(select_string);
    console.log(select, "string")
    if (checked == true){
        select[0].selectedIndex = 1;
    }
    else{
        select[0].selectedIndex = 0;
    }
}
//function checkBoxCheck() {
//    var button = $('#registration_form #a-submit');
//    if ($('input[name="nb_ticket[]"]:checked').length) {
//        button.attr('disabled', false);
//    } else {
//        button.attr('disabled', true);
//    }
//}
function array() {
    var input = document.getElementsByName('nb_ticket[]');
    var a =[]
    for (var i = 0; i < input.length; i++) {
        a[i] = input[i].value;
    }
    document.getElementById('ticket_ids').value = String(a);
}
function no_reg() {



    $('#no_reg_div').addClass('d-none');
    $('#reg_form_fields').removeClass('d-none');
    $('#o_wevent_tickets').removeClass('d-none');
    $('#candidate_no_div').removeClass('d-none');
    $('#o_wevent_tickets').addClass('bg-white shadow-sm o_wevent_js_ticket_details');
    var limit = document.getElementById('limit').value;
    if (limit == 1){
        $('#next_reg').html('Continue');
    }
    $('#heading_section').html('Child\'s Details');

}
count = 1;
function next_reg_fun() {
    if (document.getElementById('u_name').value == ''){
        $('#u_name').addClass('warning_placeholder');
        document.getElementById('u_name').placeholder = "Type name here.";
        return;
    }
    else{
        document.getElementById('u_name').placeholder = "";
    }
    if (document.getElementById('u_email').value == ''){
        $('#u_email').addClass('warning_placeholder');
        document.getElementById('u_email').placeholder = "Type email here.";
        return;
    }
    else{
        document.getElementById('u_email').placeholder = "";
    }
    if (document.getElementById('u_med_info').value == ''){
        $('#u_med_info').addClass('warning_placeholder');
        document.getElementById('u_med_info').placeholder = "Type Medical Information.";
        return;
    }
    else{
        document.getElementById('u_med_info').placeholder = "";
    }
    if (document.getElementById('u_dob').value == ''){
        $('#u_dob_label').html('Enter Date of Birth');
        document.getElementById('u_dob_label').style.color = '#dc3545';
        return;
    }
    else{
         $('#u_dob_label').html('Date of Birth');
        document.getElementById('u_dob_label').style.color = '#212529';
    }


    var button = $('#registration_form #a-submit');
    if ($('input[name="nb_ticket[]"]:checked').length) {
        if(!$('#checkbox_alert').hasClass('d-none')){
            $('#checkbox_alert').addClass('d-none');
        }
    }
    else {
        $('#checkbox_alert').removeClass('d-none');
        return;
    }

    num = count+1 % 10;
    if(num == 1){
        $('#candidate_no').html('Enter '+ (count+1) + 'st'+' Candidate Details');
    }
    else if(num == 2){
        $('#candidate_no').html('Enter '+ (count+1) + 'nd'+' Candidate Details');
    }
    else if(num == 3){
        $('#candidate_no').html('Enter '+ (count+1) + 'rd'+' Candidate Details');
    }
    else{
        $('#candidate_no').html('Enter '+ (count+1) + 'th'+' Candidate Details');
    }


    u_name[count-1] = document.getElementById('u_name').value;
    email[count-1] = document.getElementById('u_email').value;
    phone[count-1] = document.getElementById('u_phone').value;
    dob[count-1] = document.getElementById('u_dob').value;
    med_info[count-1] = document.getElementById('u_med_info').value;
    var input = document.getElementsByName('nb_ticket[]');
    var a =[]
    for (var i = 0; i < input.length; i++) {
        if (input[i].checked){
            a[i] = input[i].value;
        }
        else{
            a[i] = 0;
        }
    }
    var a_filtered = a.filter(function (el) {
        return el != null;
    });
    event_ticket_ids[count-1] = '['+String(a_filtered)+']';
    console.log(event_ticket_ids, document.getElementById('user_ticket_ids'));
    document.getElementById('user_ticket_ids').value = String(event_ticket_ids);
    document.getElementById('user_email').value = String(email);
    document.getElementById('user_name').value = String(u_name);
    document.getElementById('user_phone').value = String(phone);
    document.getElementById('user_dob').value = String(dob);
    document.getElementById('user_med_info').value = String(med_info);
    count += 1;
    var limit = document.getElementById('limit').value;
    if (count == limit){
        $('#next_reg').html('Continue');
    }
    if (count > limit){
        $('#heading_section').html('Parent\'s Details');
        $('#parent_info_form').removeClass('d-none');
        $('#parent_info_form').addClass('d-block');
        $('#reg_form_fields').addClass('d-none');
        $('#o_wevent_tickets').addClass('d-none');
        $('#candidate_no_div').addClass('d-none');
//        var canvas = document.getElementById("sig-canvas");
//        var ratio =  Math.max(window.devicePixelRatio || 1, 1);
//
//        // This part causes the canvas to be cleared
//        canvas.width = canvas.offsetWidth * ratio;
//        canvas.height = canvas.offsetHeight * ratio;
//        canvas.getContext("2d").scale(ratio, ratio);
//        window.onresize = resizeCanvas;
//        resizeCanvas();
    }
    $('#u_name').val('');
    $('#u_email').val('');
    $('#u_phone').val('');
    $('#u_dob').val('');
    $('#u_med_info').val('');


    $('input[name="nb_ticket[]"]:checked').each(function () {
        this.checked = false;
    });
}

function submit_form_fun(){
    if (document.getElementById('par_name').value == ''){
        $('#par_name').addClass('warning_placeholder');
        document.getElementById('par_name').placeholder = "Type name here.";
        return;
    }
    else{
        document.getElementById('par_name').placeholder = "";
    }
    if (document.getElementById('par_email').value == ''){
        $('#par_email').addClass('warning_placeholder');
        document.getElementById('par_email').placeholder = "Type email here.";
        return;
    }
    else{
        document.getElementById('par_email').placeholder = "";
    }
    if (document.getElementById('par_phone').value == ''){
        $('#par_phone').addClass('warning_placeholder');
        document.getElementById('par_phone').placeholder = "Type phone here.";
        return;
    }
    else{
        document.getElementById('par_phone').placeholder = "";
    }
    if (document.getElementById('emergency_no_1').value == ''){
        $('#emergency_no_1').addClass('warning_placeholder');
        document.getElementById('emergency_no_1').placeholder = "Type phone here.";
        return;
    }
    else{
        document.getElementById('emergency_no_1').placeholder = "";
    }
    var canvas = document.getElementById("sig-canvas");
    var dataUrl = canvas.toDataURL();
    var sigText = document.getElementById("sig-dataUrl");
    sigText.value = dataUrl;

//    $('#par_name').val('');
//    $('#par_email').val('');
//    $('#par_phone').val('');
//    $('#emergency_no_1').val('');
    $('#t_c').checked = false;
    var event_id =  $('#event_id').val()
    console.log(event_id)
    if (confirm('Do you want to submit?')) {
           $('#registration_form').attr('action', '/event/registration/new_event');
           document.getElementById("registration_form").submit();
       }
       else {
            location.reload();
            return false;
       }
       $('#entire_form').addClass('d-none');
       $('#next_reg').addClass('d-none');
       $('#registration_form #a-submit').attr('disabled', false);
       $('#thank_section').removeClass('d-none');
       $('#reg_form_fields').addClass('d-none');
       $('#o_wevent_tickets').addClass('d-none');
}
function t_c_check(){
    if (document.getElementById('t_c').checked){
        $('#submit_form_id').attr('disabled', false);
    }
    else{
        $('#submit_form_id').attr('disabled', true);
    }
}
