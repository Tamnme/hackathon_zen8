const { WebClient } = require("@slack/web-api");

// Helper function to format timestamp
const formatTimestamp = (timestamp) => {
  const date = new Date(parseFloat(timestamp) * 1000);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};

// Helper function to generate message link
const generateMessageLink = (teamDomain, channelId, timestamp) => {
  const urlTimestamp = timestamp.replace(".", "");
  return `https://${teamDomain}.slack.com/archives/${channelId}/p${urlTimestamp}`;
};

// Helper function to get team info
const getTeamInfo = async (slack) => {
  try {
    const result = await slack.auth.test();
    return {
      id: result.team_id,
      domain: result.team_domain || result.team,
    };
  } catch (error) {
    console.error("Error fetching team info:", error);
    return null;
  }
};

// Helper function to get user info
const getUserInfo = async (userId, slack) => {
  try {
    const userResult = await slack.users.info({ user: userId });
    if (userResult.ok) {
      const user = userResult.user;
      return {
        id: user.id,
        name: user.name,
        real_name: user.real_name,
        display_name: user.profile.display_name || user.real_name,
      };
    }
  } catch (error) {
    console.error(`Error fetching info for user ${userId}:`, error);
  }
  return {
    id: userId,
    name: "Unknown",
    real_name: "Unknown",
    display_name: "Unknown",
  };
};

// Helper function to fetch thread replies
const fetchThreadReplies = async (channelId, threadTs, slack) => {
  try {
    const result = await slack.conversations.replies({
      channel: channelId,
      ts: threadTs,
    });

    const replies = [];
    for (const msg of result.messages) {
      if (msg.ts === threadTs) continue;

      const userInfo = await getUserInfo(msg.user, slack);
      replies.push({
        ts: msg.ts,
        user_name: userInfo.display_name || userInfo.real_name || userInfo.name,
        content: msg.text,
      });
    }

    return replies;
  } catch (error) {
    console.error(`Error fetching thread replies for ${threadTs}:`, error);
    return [];
  }
};

exports.handler = async (event) => {
  try {
    const { channels, limit, oldest, latest, inclusive, cursor, token } =
      event.queryStringParameters || {};

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

    if (!channels) {
      return {
        statusCode: 400,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify({
          error:
            "Channel IDs are required. Use comma-separated values for multiple channels",
        }),
      };
    }

    const slack = new WebClient(token);
    const teamInfo = await getTeamInfo(slack);

    if (!teamInfo) {
      return {
        statusCode: 500,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify({
          error: "Failed to get team information",
        }),
      };
    }

    const channelIds = channels.split(",");
    const channelPromises = channelIds.map(async (channelId) => {
      try {
        const result = await slack.conversations.history({
          channel: channelId,
          limit: parseInt(limit) || 100,
          oldest: oldest || undefined,
          latest: latest || undefined,
          inclusive: inclusive === "true",
          cursor: cursor || undefined,
        });

        const messages = await Promise.all(
          result.messages.map(async (msg) => {
            const userInfo = await getUserInfo(msg.user, slack);
            const timeFormatted = formatTimestamp(msg.ts);
            const messageLink = generateMessageLink(
              teamInfo.domain,
              channelId,
              msg.ts
            );

            let messageText = msg.text;
            if (msg.subtype === "channel_join") {
              messageText = `${
                userInfo.display_name || userInfo.real_name || userInfo.name
              } has joined the channel`;
            }

            let messageString = `${timeFormatted} | ${
              userInfo.display_name || userInfo.real_name || userInfo.name
            } | ${messageText} | ${messageLink}`;

            if (msg.reply_count > 0) {
              const replies = await fetchThreadReplies(
                channelId,
                msg.ts,
                slack
              );
              const replyStrings = replies.map((reply) => {
                const replyLink = generateMessageLink(
                  teamInfo.domain,
                  channelId,
                  reply.ts
                );
                return `        | ${formatTimestamp(reply.ts)} | ${
                  reply.user_name
                } | ${reply.content} | ${replyLink}`;
              });
              messageString += "\n" + replyStrings.join("\n");
            }

            return messageString;
          })
        );

        return {
          channelId,
          messages,
        };
      } catch (error) {
        console.error(`Error crawling channel ${channelId}:`, error);
        return {
          channelId,
          error: error.message,
          messages: [],
        };
      }
    });

    const results = await Promise.all(channelPromises);
    const groupedMessages = results.reduce((acc, result) => {
      acc[result.channelId] = result.messages;
      return acc;
    }, {});

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
      body: JSON.stringify(groupedMessages),
    };
  } catch (error) {
    console.error("Error crawling messages:", error);
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
