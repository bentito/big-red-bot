import requests
import json

# Note: You need to replace 'your-slack-api-token' with your actual Slack API token
# and 'your-search-query' with the term you want to search for.
slack_token = 'your-slack-api-token'
search_query = 'your-search-query'

def search_slack(query, token):
    url = 'https://slack.com/api/search.messages'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'query': query,
        'sort': 'score',
        'sort_dir': 'desc'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Example usage
# Replace 'your-slack-api-token' and 'your-search-query' with actual values
result = search_slack(search_query, slack_token)

# This will print the result. You might want to process it further depending on your needs.
print(json.dumps(result, indent=4))
