<div>
    Date:
    <asp:TextBox ID="txtDate" runat="server" class="date-format"></asp:TextBox>
    <asp:Button ID="btnValidate" runat="server" Text="Validate" OnClientClick="Validate();" />
</div>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.maskedinput/1.4.1/jquery.maskedinput.js"></script>
<script type="text/javascript">
    $(document).ready(function () {
        $('#txtDate').mask("99/99/9999", { placeholder: 'DD/MM/YYYY' });
 
    });
    function Validate() {
        var date = document.getElementById("txtDate").value.split("/");
        var day = date[0];
        var month = date[1];
        var dateString = document.getElementById("txtDate").value;
        var regex = /^(0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])[\/\-]\d{4}$/;
        if (regex.test(dateString) || dateString.length == 0) {
            alert("Please enter correct date");
 
        }
        if (day > 31) {
            alert("Please enter correct date");
        }
        else
            if (month > 12) {
                alert("Please enter correct date");
            }
    }
</script>