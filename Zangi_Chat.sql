--SQLite query for parsing Zangi Chats from iOS
select
	    datetime(ZZANGIMESSAGE.ZMESSAGETIME+978307200, 'unixepoch') AS 'MESSAGE DATE/TIME',
	    ZCONTACT.ZFIRSTNAME,
	    ZCONTACT.ZLASTNAME,
	    ZZANGIMESSAGE.ZMESSAGE,
	    CASE ZZANGIMESSAGE.ZISRECEIVED
	    WHEN '0' THEN 'SENT'
	    WHEN '1' THEN 'RECEIVED'
	    ELSE 'unknown'
	    END AS DIRECTION,
	    ZZNUMBER.ZNUMBER
	    FROM ZZANGIMESSAGE
	    JOIN ZZNUMBER ON ZZANGIMESSAGE.ZFROM = ZZNUMBER.ZCONTACTNUMBEROBJECT
	    left JOIN ZCONTACT ON ZZNUMBER.ZIDENTIFIRE = ZCONTACT.ZIDENTIFIRE
	    order by ZZANGIMESSAGE.ZMESSAGETIME DESC;