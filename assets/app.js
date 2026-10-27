const $=id=>document.getElementById(id);
$('searchBtn').addEventListener('click',()=>{$('status').textContent='Поиск выполнен локально. Запрос: '+($('searchInput').value||'(пусто)');});
$('openDialog').addEventListener('click',()=>$('dialog').showModal());
$('closeDialog').addEventListener('click',()=>{$('dialog').close();$('openDialog').focus();});
$('openWindow').addEventListener('click',()=>{const w=window.open('../help.html','lab1-help','popup,width=620,height=500');if(!w)$('status').textContent='Окно заблокировано браузером. Разрешите всплывающее окно для этой страницы.';});
