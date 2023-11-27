// expressionEvaluatorSafe.js

module.exports = (function () {
  function maskedEval(expression, context) {
    const maskedContext = Object.create(null);

    for (let prop in globalThis) {
      maskedContext[prop] = undefined;
    }

    for (let prop in context) {
      if (context.hasOwnProperty(prop)) {
        maskedContext[prop] = context[prop];
      }
    }

    return new Function("context", `with(context) { return ${expression} }`)(maskedContext);
  }

  return {
    evaluateExpression: maskedEval,
  };
})();
