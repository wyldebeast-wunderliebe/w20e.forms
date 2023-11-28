// expressionEvaluatorSafe.js

module.exports = (function () {
  function maskedEval(expression, context) {

    try {
        const contextKeys = Object.keys(context);
        const contextValues = contextKeys.map(key => context[key]);

        // Create a function with the provided expression and context variables
        const evalFunction = new Function(...contextKeys, `return ${expression}`);
        const result = evalFunction(...contextValues);
        return result;
    } catch (error) {
        // Handle any errors that may occur during evaluation
        console.error('Error evaluating expression:', error.message);
        return null;
    }
  }

  return {
    evaluateExpression: maskedEval,
  };
})();
