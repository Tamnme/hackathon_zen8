const { WebClient } = require("@slack/web-api");

exports.handler = async (event) => {
  try {
    const { token, email, name } = event.queryStringParameters || {};

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
    const result = await slack.users.list();

    if (!result.ok) {
      return {
        statusCode: 500,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify({
          error: "Failed to get users information",
        }),
      };
    }

    let users = result.members.map((user) => ({
      id: user.id,
      name: user.name,
      real_name: user.real_name,
      display_name: user.profile.display_name || user.real_name,
      email: user.profile.email || null,
      avatar: user.profile.image_192 || null,
    }));

    if (email) {
      users = users.filter(
        (user) =>
          user.email && user.email.toLowerCase().includes(email.toLowerCase())
      );
    }

    if (name) {
      users = users.filter(
        (user) =>
          user.name.toLowerCase().includes(name.toLowerCase()) ||
          user.real_name.toLowerCase().includes(name.toLowerCase()) ||
          user.display_name.toLowerCase().includes(name.toLowerCase())
      );
    }

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
      body: JSON.stringify(users),
    };
  } catch (error) {
    console.error("Error fetching users information:", error);
    return {
      statusCode: 500,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
      body: JSON.stringify({
        error: error.message,
        slack_error_code: error.data?.error || null,
      }),
    };
  }
};
