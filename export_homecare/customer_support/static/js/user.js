
  $(document).ready(function(){
      $(document).on('click', '.edit', function(){
          var id = $(this).data('id');
          
          var name = $('#name' + id).text();
       
          var phone = $('#phone' + id).text();
          var email = $('#email' + id).text();
          var gender = $('#gender' + id).text();
          var status = $('#status' + id).text();
          console.log(email);
  
          $('#editModal').modal('show');
          $('#modal_name').val(name);
          $('#modal_email').val(email);
          $('#modal_phone').val(phone);        
          $('#modal_gender').val(gender);
          $('#modal_status').val(status);
          $('#modal_id').val(id);
      });
  });
