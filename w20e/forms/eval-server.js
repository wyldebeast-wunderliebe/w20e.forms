const http = require('http');
const { parse } = require('querystring');
const { runInNewContext } = require('vm');

// Method registry
const methodRegistry = {
  sample: (array, size) => {
    const shuffled = array.slice(0);
    let i = array.length;
    let rand;
    const result = [];

    while (i-- > 0) {
      rand = Math.floor((i + 1) * Math.random());
      [shuffled[i], shuffled[rand]] = [shuffled[rand], shuffled[i]];
    }

    for (let j = 0; j < size; j++) {
      result.push(shuffled[j]);
    }

    return result;
  },

  // Add more methods as needed
  // method2: (params) => { ... },
  // method3: (params) => { ... },
};

// Get the port from command-line arguments using --port or use a default value (3000)
const portIndex = process.argv.indexOf('--port');
const port = portIndex !== -1 ? process.argv[portIndex + 1] : 3000;

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/evaluate') {
    let data = '';

    req.on('data', chunk => {
      data += chunk.toString();
    });

    req.on('end', () => {
      try {
        const { expression, context } = JSON.parse(data);

        if (!expression || !context) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Expression and context are required' }));
          return;
        }

        // Extend the context with the method registry
        const evaluationContext = { ...context, ...methodRegistry };

        const result = runInNewContext(expression, evaluationContext);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ result }));
      } catch (error) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
      }
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

server.listen(port, () => {
  console.log(`Server is listening at http://localhost:${port}`);
});


