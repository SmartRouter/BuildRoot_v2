### Lighttpd Configuration File

# modules to load
server.modules = (	"mod_access",
			"mod_accesslog",
			"mod_alias",
			"mod_compress",
			"mod_fastcgi",
			"mod_flv_streaming",
			"mod_cgi",
			"mod_status",
			"mod_auth"
)

# files to check for if .../ is requested
index-file.names = (	"index.php", "index.cgi",
			"index.htm", "index.html"
)
# mimetype mapping
mimetype.assign = (	".png"  => "image/png",
			".jpg"  => "image/jpeg",
			".jpeg" => "image/jpeg",
			".html" => "text/html",
			".htm"  => "text/html",
			".txt"  => "text/plain",
			".css"  => "text/css",
			""      => "text/plain"
)
# CGI module
cgi.assign = ( ".cgi"  => "/bin/sh" )

flv-streaming.extensions = ( ".flv" )
server.document-root		= "/var/http/htdocs/"
status.status-url		= "/server-status"
status.config-url		= "/server-config"
status.statistics-url	= "/server-statistics"
server.pid-file		= "/var/run/lighttpd.pid"
server.tag			= "Lighttpd | TextDriven"
accesslog.filename		= "/dev/null"
server.errorlog		= "/dev/null"
server.max-keep-alive-request = 0
server.max-keep-alive-idle =0
