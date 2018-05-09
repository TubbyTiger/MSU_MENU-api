var app = express()
var port = process.env.PORT || 8080
var bodyParser = require('body-parser')

app.listen(port)
app.use(bodyParser.json())

// GET
app.get('/', function (request, response, body) {
  var menu = JSON.parse(fs.readFileSync('menu.json', 'utf8'));
  response.json(menu)
})
