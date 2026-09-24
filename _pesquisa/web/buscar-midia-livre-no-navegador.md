# 🔎 Pesquisa: buscar-midia-livre-no-navegador

> Busca: `Openverse API CORS browser fetch openly licensed images Wikimedia Commons API origin=* CORS image search free API no key`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## API:Cross-site requests - MediaWiki

`https://www.mediawiki.org/wiki/API:Cross-site_requests`

Get the current user's watchlist as a feed

Advanced search for wiki pages by title or text

Using the API in MediaWiki and extensions

If an external site needs to make an API call against a MediaWiki site, it must use

If a user script or gadget is used to make an API call against a site within the same

, it must use a MediaWiki module that uses CORS under the hook:

This is the way to go, for instance, if a script on the English Wikipedia needs to check image information on Commons.

The rest of this section is for developers who cannot use

If the CORS request is authenticated via cookies, the

value must be the site from which the request originates, which is matched against the Origin header required by the CORS protocol.

Note that these parameters must be included in any

, and so should be included in the query string portion of the request URI even for POST requests.

parameter is supplied and the request does not return a successful CORS response, MediaWiki≥1.30  will return a

header with a brief reason for the failure, e.g. in case of mismatched origin or unsupported headers in a

Unauthenticated CORS requests may be made from any origin by setting the

header in the response and will process the request as if logged out.

Get the names of the first three images from Wikimedia Commons.

"https://commons.wikimedia.org/w/api.php"

"action=query&list=allimages&ailimit=3&format=json"

// Process the output to get the image names

!!!!!_Mdina_Fortifications,_Ditch,_Bridge_and_Main_Gate.jpg

!!!!_Palazzo_Dorell_ancillary_building.jpg

Authenticated CORS Requests using cookies

To make an authenticated CORS request using cookies, the remote wiki's

setting must be set to allow the origin site, and the

parameter must be set to the origin site in the request URL.

If the CORS origin check passes, MediaWiki will include the

header in the response, so authentication cookies may be sent.

To make an authenticated CORS request using

, obtain an OAuth access token using the normal authorization flow, then make the request with

in the request URL (no value necessary) and

contains more instructions and examples on how to handle CORS requests in JavaScript.

parameter, whose value is a JavaScript function which the JSON result will be wrapped in.

This may be used to call the API on a remote site by dynamically adding

Using JSONP weakens the security of your origin site because, as described above, API responses are executed as JavaScript code. If an attacker compromises the

, they can use their access to run arbitrary JavaScript code in your users' browsers, within the context of

Any JSONP requests will be processed as if logged out (i.e as an anonymous user), even after logging in to the remote wiki.

Get the titles of three random pages from English Wikipedia.

"action=query&list=random&rnlimit=3&format=json"

Extension:CentralAuth/API#centralauthtoken

https://www.mediawiki.org/w/index.php?title=API:Cross-site_requests&oldid=7794831

---

## ⚠️ Paginas que NAO deram texto

- `https://api.openverse.org/v1/images/?q=floresta&page_size=3` — HTTP 200
- `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=filetype:bitmap%20floresta&gsrlimit=3&prop=imageinfo&iiprop=url|extmetadata&format=json&origin=*` — HTTP 200
- `https://docs.openverse.org/` — bloqueada ou vazia
- `https://api.openverse.org/v1/` — bloqueada ou vazia
- `https://bytetools.bytevancer.com/public-apis/photography/openverse-api` — HTTP 403
