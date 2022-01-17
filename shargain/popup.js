// Initialize button with users's prefered color
const host = 'https://shargain-hackathon.beyondthe.dev';
// const host = 'http://192.168.3.221:8000'
const sendButton = document.getElementById("send-button");

// chrome.storage.sync.get("color", ({color}) => {
//   changeColor.style.backgroundColor = color;
// });

document.getElementById('channel-dropdown').style.display = 'none';
document.getElementById('target-name-existing').style.display = 'none';

document.getElementById('target-notifications').addEventListener('change', (event) => {
  document.getElementById('channel-dropdown').style.display = event.currentTarget.checked ? '' : 'none';
})

document.getElementById('target-existing').addEventListener('change', (event) => {
  document.getElementById('target-name-new').style.display = event.currentTarget.checked ? 'none' : '';
  document.getElementById('target-name-existing').style.display = event.currentTarget.checked ? '' : 'none';
})

const setDefaultValues = async () => {
  let [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  document.getElementById("target-name").value = tab.title;
  document.getElementById("target-url").value = tab.url;

  const channels = (await axios.get(`${host}/api/notification-configs/`)).data;

  const targets = (await axios.get(`${host}/api/scrapping-targets/`)).data;

  console.log(targets);

  const channelsDropdown = document.getElementById("target-channel");
  channels.forEach(({
                      id,
                      name,
                      channel
                    }) => channelsDropdown.innerHTML += `<option value="${id}">${name} (${channel})</option>`);

  const targetsDropdown = document.getElementById("target-name-select");
  targets.forEach(({id, name}) => targetsDropdown.innerHTML += `<option value="${id}">${name}</option>`);
}

setDefaultValues();

// When the button is clicked, inject setPageBackgroundColor into current page
sendButton.addEventListener("click", async () => {
  const successMessage = document.getElementById('success-message');
  const errorMessage = document.getElementById('error-message');

  successMessage.style.display = 'none';
  errorMessage.style.display = 'none';

  const addToExisting = document.getElementById('target-existing').checked;
  const targetName = document.getElementById("target-name").value;
  const targetNameExisting = document.getElementById("target-name-select").value;
  const targetUrl = document.getElementById("target-url").value;
  const enableNotifications = document.getElementById('target-notifications').checked;
  const channel = document.getElementById("target-channel").value;

  const data = addToExisting ? {
    url: targetUrl,
  } : {
    name: targetName,
    url: [targetUrl],
    enable_notifications: enableNotifications,
    notification_config: enableNotifications ? channel : null
  };


  const endpoint = addToExisting ? `${host}/api/scrapping-targets/${targetNameExisting}/add-target-url/` : `${host}/api/scrapping-targets/`;

  try {
    await
      axios.post(endpoint, data);
    successMessage.style.display = 'block';
  } catch (e) {
    errorMessage.style.display = 'block';
  }


  // chrome.scripting.executeScript({
  //   target: {tabId: tab.id},
  //   function: setPageBackgroundColor,
  // });
});

// The body of this function will be execuetd as a content script inside the
// current page
function setPageBackgroundColor() {
  chrome.storage.sync.get("color", ({color}) => {
    document.body.style.backgroundColor = color;
  });
}
