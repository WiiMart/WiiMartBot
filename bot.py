import discord
from discord.ext import commands
import os
from dotenv import load_dotenv 
import sqlite3
import mysql.connector
from mysql.connector import Error
import re
import requests


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix="/", intents=intents, case_insensitive=True)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.tree.sync()

load_dotenv()
intents = discord.Intents.all()
bot = Bot(intents=intents)
client = discord.Client(intents=intents)
token = os.getenv("token")
status = os.getenv("status")
url_status = "Unknown"
url = "https://oss-auth.blinklab.com/"

error_codes = """
201005: Invalid public key type in certificate
201009: Read failure (short read)
201010: Write failure (short write)
201012: Invalid signature type (for signed blobs)
201016: Maximum amount of handles exceeded (3 handles, as there are only 3 contexts)
201017: Invalid arguments
201020: Device ID mismatch. Returned by ES_ImportTicket if the ticket is personalised and the device ID from the ticket mismatches with the actual ID.
201022: Imported content hash does not match with the hash from the TMD. Returned by ES_ImportContentEnd and ES_ImportBoot.
201024: Memory allocation failure
201026: Incorrect access rights (according to the TMD)
201027: Issuer not found in the certificate chain
201028: Ticket not found
201029: Invalid ticket. This is returned if the common key field contains an invalid value (anything other than 0 or 1). This is also returned from ES_LaunchTitle if the title ID contained in the ticket does not match the TMD title ID.
201031: During LaunchTitle/ImportTitle: installed boot2 version is too old. During ImportBoot: downgrades are not allowed.
201032: Fatal error early in ES initialisation. Can also be returned in ES_CheckHasKoreanKey in all other cases (key is not the Korean Key or a zero key!)
201033: A ticket limit was exceeded (duration or launch count)
201034: Returned by ES_CheckHasKoreanKey if the key is sensed to be all zeroes
201035: A title with a higher version is already installed
201036: Required sysversion(IOS) is not installed (only for the system menu [check])
201037: Installed number of contents doesn't match TMD (only for the system menu [check])
201039: Returned by DI as an ES error code when TMD not supplied for disc/nand game
202000: Permission denied (returned when accessing an object for which the caller has no permission)
202001: IOSC_EEXIST
202003: IOSC_EMAX
202004: IOSC_ENOENT
202005: IOSC_INVALID_OBJTYPE
202006: IOSC_INVALID_RNG
202007: IOSC_INVALID_FLAG
202008: IOSC_INVALID_FORMAT
202009: IOSC_INVALID_VERSION
202010: IOSC_INVALID_SIGNER
202011: IOSC_FAIL_CHECKVALUE
202012: Internal failure
202013: Memory allocation failure. Known to be returned when the keyring is full (contains 0x20 keys)
202014: Invalid size
202015: Invalid address
202016: Unaligned data
204013: Try another credit card or contact your credit card provider
204017: Wii Points Card invalid
204038: Wireless interferences?
204042: User is not registered with the server
204961: SSL cipher error when trying to communicate with SOAP servers
204050: You do not own a title; ticket not found
204036: Problem importing title metadata
204035: Problem importing ticket
204037: Problem importing title content
204034: Invalid SOAP response
204501: HTTP 201 Created
204502: HTTP 202 Accepted
204503: HTTP 203 Non-Authoritative Information
204504: HTTP 204 No Content
204505: HTTP 205 Reset Content
204506: HTTP 206 Partial Content
204600: HTTP 300 Multiple Choices
204601: HTTP 301 Moved Permanently
204602: HTTP 302 Found
204603: HTTP 303 See Other
204604: HTTP 304 Not Modified
204607: HTTP 307 Temporary Redirect
204608: HTTP 308 Permanent Redirect
204700: HTTP 400 Bad Request
204701: HTTP 401 Unauthorized
204702: HTTP 402 Payment Required
204703: HTTP 403 Forbidden
204704: HTTP 404 Not Found
204705: HTTP 405 Method Not Allowed
204706: HTTP 406 Not Acceptable
204707: HTTP 407 Proxy Authentication Required
204708: HTTP 408 Request Timeout
204709: HTTP 409 Conflict
204710: HTTP 410 Gone
204711: HTTP 411 Length Required
204712: HTTP 412 Precondition Failed
204713: HTTP 413 Request Too Large
204714: HTTP 414 Request-URI Too Long
204715: HTTP 415 Unsupported Media Type
204716: HTTP 416 Range Not Satisfiable
204717: HTTP 417 Expectation Failed
204800: HTTP 500 Internal Server Error
204801: HTTP 501 Not Implemented
204802: HTTP 502 Bad Gateway
204803: HTTP 503 Service Unavailable
204804: HTTP 504 Gateway Timeout
204805: HTTP 505 HTTP Version Not Supported
204811: HTTP 511 Network Authentication Required
204900-204959: NHTTP Error range
204960-204979: EC SSL Error range
20955X: 2-7 Timeout occurred between client and server
204704: Equivalent to a HTTP 404 error
2056XX: ECS Error
205625: ECS Gift error
2059XX-2064XX: IAS Error
205968: "Bad device code" (?)
205627: Cannot buy DLC for a title you don't own
2057XX-20570X: ETS Error
2058XX-205825: PAS Error
2066XX: OSS Error
209531: Page was not found
209622: SSL CA unknown / not included in channel
220003: The requested URL was filtered by Opera's filter
204927: IAS Unknown issuer of device cert
204901-204973: Try another credit card or contact your credit card provider
205540: This software doesn't work in the vWii
205617: Wii Points card code invalid
205618: Wii Points card is for another country
205621: Unknown error (possibly ECS gift error?)
205623: Trial period for that title expired, you can't download that again
205626: Unable to send present (ECS gift error)
205642: Unknown error
205643: Unknown error
205644: Credit cards can't be used on this console.
205645: Issue with your DSi shop account?
205646: Unable to send present (ECS gift error)
205672: Wii Shop account mismatch
20580X: Wii Points Card error
205810: You don't have enough Wii Points / Error while redeeming your download ticket
205811: Wii Points card expired
205812-205814: The Wii Points card can not be used
205815: Wii Points Card was already used
205816: Some error with the Wii Points Card
205818: This card number can only be used for a specific title, it is not a Wii Points Card.
205819: Wii Points Card code is invalid
205830: Wii Points Card code is invalid
205831: Wii Points Card is for another Country
205901: Wii number invalid!
205903: Unknown error
205906: Problem with your online account
205921-205925: Wii NAND corrupted
205928: Unknown error
205940-250941: Problems with your "Club-Nintendo"-account. It can't get connected with your shop account
250943: Problems with your "Club-Nintendo"-account. It can't get connected with your shop account
209600-209601: Connection timeout
205942: Maintenance. Login not possible
205958: Unknown error
205968: IAS_BAD_DEVICE_CODE
206112: The free title promotion has ended (ICR_END)
206401: Invalid characters in nick or password
206499: Maintenance. Login not possible
206601: OSS_ERROR_INVALID_PARAM. Triggered by B_24 in Wii Shop (Invalid parameter)
206602: Error while entering Wii Points Card code. Try again later.
206603: Unable to confirm credit card information
206607: Error while retrieving the served content
206608: Error redeeming Wii Download Ticket
206610: Wii download ticket expired
206611: Wii download ticket invalid
206612: This Wii download ticket can't be used in your country
206613: No software available for this download ticket. May be caused by parental controls.
206650: Wrong PIN (parental controls)
206651: Mistake while entering the wii serial number
206652: Wrong PIN three times (parental controls)
206653: Nickname or password wrong
206660: No progress was made in the last operation
206661: Credit card type invalid
206662: Credit card number invalid
206663: An operation is in progress
206664: No security code was provided
206667: Wii download ticket invalid
206668: Happens when current points count + new points would exceed the wii points limit
206669: Wii Points card invalid
206670: Problem with your Wii Shop Account (invalid Wii number)
206671: Problem with your Wii Shop Account (invalid shop app - bad title ID)
206672: Problem with your Wii Shop Account (invalid shop app - no title info)
206673: Problem with your Wii Shop Account (invalid registration status)
206674: Problem with your Wii Shop Account (unexpected eclib error)
206699: Try again later
208000: You have entered the wrong state ("Bundesland")
208001: Unable to process for credit cards (some kind of blacklist?)
208002: Billing address invalid
208003: Credit card number doesn't match card type
208004: three-digit security code invalid
208005: Mistake in credit card data.
208006: Card number invalid
208007: Expiration date invalid
208008: Postal code invalid
208009: Technical difficulties.
208010: Credit card could not get validated. Try again later.
208011: Credit card declined
208012: Credit card declined - no funds available
208013: Credit card declined - inactive
208014: Credit card expired
208015: Credit card code invalid
208016: Credit card number invalid
208017: Credit card limit reached
208018: Credit card invalid
208019: Postal / zip code invalid
208021: Refund is in progress
208022: Refund was already processed
208023: Refund error
208025: Empty security code
209XXX: Server connection timeout
209531: Web page not found (WS_ERROR_WWW_HTTP_ERR_NOT_FOUND)
209552: Timeout between client and server
209557: Timeout Occurred between client and server
209593: Access denied by Opera Wii Shop domain filter config
209620: Some JS files couldn't be loaded (CheckRegistered.jsp line ~100)
209622: SSL CA unknown / not included in channel
209631: Invalid SD Card
209632: The SD Card is inserted(?)
209633: The SD Card is not inserted
209634: Unknown SD Card cluster (not 32k)
209635: Incorrect SD Card alignment
209636: Incorrect SD Card Device
209637: The title's ticket is not present on the SD
209638: SDCARD_ERROR_ACCESS
209639: SDCARD_ERROR_CANCELLED (cancelBackupToSDCard successful?)
209640: SDCARD_ERROR_CONTENT_INVALID (Banner is not found)
209641: SDCARD_ERROR_MAXFD (?)
209642: The SD Card is "out of memory"
209643: The SD Card is corrupted (NAND_CORRUPT ERROR (Serious error))
209644: SDCARD_ERROR_ECC_CRIT (?)
209645: SD Authentication error(?)
209646: Fatal error with the SD Card
209647: Unknown SD Card
209648: The SD Card is not inserted
209649: The SD Card is not supported
209650: SD Card File system is broken
209651: SD is write protected
209652: No space left in the SD
209653: Other SD error
209654: Unknown SD Error
209655: SDCARD_ERROR_WANT_OF_CAPACITY (SD full)
209656: SDCARD_ERROR_EXIST_CHECK_SOFT (title already present on SD)
209657: SDCARD_ERROR_EXCEPTION_STATE (Illegal statement and cancelBackupToSDCard error)
209658-209660: Unused
209661: EXIST_CHECK_SOFT_NAND
209662: errChannel
209663: errInodes
209664: SD Backup timeout in B-10
209665: JournalFlag error in B-10
209666: Available space error in B-09 on checking remain size
209667: Available space is not sufficient (NAND)
209800 - 209801: Connection timeout (also caused by missing shop.connecting)
220000: Connection failed
220001: Unknown protocol
220002: Out of memory
220101: Allocation error
220102: Unsupported file
220103: Empty file
220104: Invalid file
220105: Javascript error
220106: Plugin error
220201: Not found
220202: Connection refused
220301-220302: HTTP error code 100 - 101
220303-220309: HTTP error code 200 - 206
220310-220315: HTTP error code 300 - 305
220316-220331: HTTP error code 400 - 415
220332-220337: HTTP error code 500 - 505
"""

def parse_error_codes(error_codes):
    exact_codes = {}
    wildcard_codes = {}

    for line in error_codes.strip().split('\n'):
        code, message = line.split(':', 1)
        code = code.strip()
        message = message.strip()

        if 'X' in code:
            wildcard_codes[code] = message
        elif '-' in code:
            # Handle ranges by expanding them into individual codes
            ranges = code.split(',')
            for r in ranges:
                r = r.strip()  # Clean up any extra spaces
                if '-' in r:  # Ensure it is a valid range
                    start, end = r.split('-')
                    start = start.strip()
                    end = end.strip()
                    # Generate all codes in the range
                    for num in range(int(start), int(end) + 1):
                        exact_codes[str(num)] = message
                else:
                    # If it's not a valid range, treat it as an exact code
                    exact_codes[r] = message
        else:
            exact_codes[code] = message

    return exact_codes, wildcard_codes

def create_database(db_name='error_codes.db'):
    # Connect to the SQLite database (or create it)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table for error codes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_codes (
            code TEXT PRIMARY KEY,
            message TEXT
        )
    ''')

    # Parse the error codes
    exact_codes, wildcard_codes = parse_error_codes(error_codes)

    # Insert exact codes into the database
    for code, message in exact_codes.items():
        cursor.execute('INSERT OR IGNORE INTO error_codes (code, message) VALUES (?, ?)', (code, message))

    # Insert wildcard codes into the database
    for code, message in wildcard_codes.items():
        cursor.execute('INSERT OR IGNORE INTO error_codes (code, message) VALUES (?, ?)', (code, message))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def matches_wildcard(code, wildcard_code):
    pattern = wildcard_code.replace('X', '[0-9]')
    return re.fullmatch(pattern, str(code)) is not None

def get_error_message(code):
    # Connect to the SQLite database
    conn = sqlite3.connect('error_codes.db')
    cursor = conn.cursor()

    # Check for exact matches
    cursor.execute('SELECT message FROM error_codes WHERE code = ?', (str(code),))
    result = cursor.fetchone()

    if result:
        return f"{code}: {result[0]}"

    # Check for wildcard matches
    cursor.execute('SELECT code, message FROM error_codes')
    for row in cursor.fetchall():
        if matches_wildcard(code, row[0]):
            return f"{code}: {row[1]}"

    return f"{code}: Error code not found."

def check_url():
    global url_status  # Declare the global variable to modify it
    try:
        response = requests.get(url, verify=False, timeout=10)  # Disable SSL verification and set a timeout
        url_status = ":green_square: Up"  # If we get a response, set status to "Up"
    except requests.exceptions.RequestException:
        url_status = ":red_square: Down"  # If there's an exception, set status to "Down"

@bot.hybrid_command(name="status",description="Gets the status of WiiMart")
async def statusy(ctx):
    check_url()
    if status == "Not Set":
        await ctx.send(f"WiiMart Status: {url_status}\nAdmin Status: :person_shrugging: Currently Unset")
    else:
        await ctx.send(f"WiiMart Status: {url_status}\nAdmin Status: {status}")

@bot.hybrid_command(name="setstatus",description="Sets the current server status to your liking")
@commands.has_any_role("Owner", "Admin", "Moderators", "Hoster")
async def setstatus(ctx, stat: str):
    global status
    status = stat
    await ctx.send(f"Status has been set to: {status}")

@bot.hybrid_command(name="unsetstatus", description="Unsets the current status")
@commands.has_any_role("Owner", "Admin", "Moderators", "Hoster")
async def unset(ctx):
    global status
    status = "Not Set"
    await ctx.send("Status has been unset.")

@bot.hybrid_command(name="error", description="Gets the error message linked with the shop error code")
async def geterror(ctx, errorcode: commands.Range[int, 200000, 250943]):
    try:
        errormessage = get_error_message(errorcode)
    except ValueError:
        errormessage = "Error Code was not found."
    await ctx.send(errormessage)

@bot.hybrid_command(name="addfc", description="Adds your Wii Friend code to the list of friend codes so that others can add you")
async def addfc(ctx, fc: int):
    await ctx.defer(ephemeral=True)
    if len(str(fc)) != 16:
        await ctx.send(f"You need to input a friendcode that is of 16 numbers not {len(str(fc))}", ephemeral=True)
    else:
        userid = ctx.author.id
        #print(userid)
        conn = mysql.connector.connect(host=os.getenv("mqur"), user=os.getenv("mqlu"), password=os.getenv("mqlp"), database=os.getenv("mqld"), port=os.getenv("mqpo"))
        cur = conn.cursor(buffered=True)
        cur.execute(f"SELECT fc FROM usersfc WHERE userid = '{userid}'")
        try:
            fethcy = cur.fetchall()
        except Error as e:
            fetchy = False
        if fethcy:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"UPDATE usersfc SET fc = '{fc}' WHERE userid = '{userid}'")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send("Updated your friend code", ephemeral=True)
        else:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"INSERT INTO usersfc (userid, fc) VALUES ('{userid}', '{fc}')")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send("Added your friend code", ephemeral=True)
    
@bot.hybrid_command(name="getfc", description="Gets the friend code of the selected user")
async def getfc(ctx, member: discord.Member):
    await ctx.defer(ephemeral=True)
    userid = member.id
    #print(userid)
    conn = mysql.connector.connect(host=os.getenv("mqur"), user=os.getenv("mqlu"), password=os.getenv("mqlp"), database=os.getenv("mqld"), port=os.getenv("mqpo"))
    cur = conn.cursor(buffered=True)
    cur.execute(f"SELECT fc FROM usersfc WHERE userid = '{userid}'")
    fetchy = cur.fetchone()[0]
    fetchy = " ".join([fetchy[i:i+4] for i in range(0, len(fetchy), 4)])
    if fetchy:
        await ctx.send(f"<@{userid}> Friend code is: {fetchy}", ephemeral=True)
    else:
        await ctx.send(f"<@{userid}> did not share his friend code.", ephemeral=True)
    cur.close()
    conn.close()

@bot.hybrid_command(name="forceaddfc", description="Force adds the users Wii Friend code to the list of friend codes so that others can add them")
@commands.has_any_role("Owner", "Admin", "Moderators")
async def addfc(ctx, user: discord.Member, fc: int):
    await ctx.defer(ephemeral=True)
    if len(str(fc)) != 16:
        userid = user.id
        await ctx.send(f"You need to input a friendcode that is of 16 numbers not {len(str(fc))} for <@{userid}>", ephemeral=True)
    else:
        userid = user.id
        #print(userid)
        conn = mysql.connector.connect(host=os.getenv("mqur"), user=os.getenv("mqlu"), password=os.getenv("mqlp"), database=os.getenv("mqld"), port=os.getenv("mqpo"))
        cur = conn.cursor(buffered=True)
        cur.execute(f"SELECT fc FROM usersfc WHERE userid = '{userid}'")
        try:
            fethcy = cur.fetchall()
        except Error as e:
            fetchy = False
        if fethcy:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"UPDATE usersfc SET fc = '{fc}' WHERE userid = '{userid}'")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send(f"Updated <@{userid}> friend code", ephemeral=True)
        else:
            cur.close()
            cur = conn.cursor(buffered=True)
            cur.execute(f"INSERT INTO usersfc (userid, fc) VALUES ('{userid}', '{fc}')")
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send(f"Added <@{userid}> friend code", ephemeral=True)

try:
    os.remove("error_codes.db")
except Exception as e:
    print("i cant let you do that dave...")
create_database()
bot.run(token)
