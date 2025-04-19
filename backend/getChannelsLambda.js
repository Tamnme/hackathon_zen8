const { WebClient } = require("@slack/web-api");

exports.handler = async (event) => {
  try {
    const { token } = event.queryStringParameters || {};

    if (!token) {
      return {
        statusCode: 400,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify({
          error: "Slack token is required",
        }),
      };
    }

    const slack = new WebClient(token);
    const result = await slack.conversations.list({
      types: "public_channel,private_channel",
    });

    const channels = result.channels.map((channel) => ({
      id: channel.id,
      name: channel.name,
    }));

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
      body: JSON.stringify(channels),
    };
  } catch (error) {
    console.error("Error fetching channels:", error);
    return {
      statusCode: 500,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
      body: JSON.stringify({
        error: error.message,
      }),
    };
  }
};
