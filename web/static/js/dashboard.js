let ws;

function connectWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateDashboard(data);
    };

    ws.onclose = function() {
        // Reconnect after 1 second
        setTimeout(connectWebSocket, 1000);
    };
}

function updateDashboard(data) {
    // Update stats
    document.getElementById('active-downloads').textContent = data.stats.active;
    document.getElementById('queued-items').textContent = data.stats.queued;
    document.getElementById('completed-today').textContent = data.stats.completed_today;

    // Update active downloads
    const activeList = document.getElementById('active-downloads-list');
    activeList.innerHTML = data.active_downloads.map(download => `
        <div class="border rounded p-4">
            <div class="flex justify-between items-center mb-2">
                <span class="font-semibold">${download.type} - ${download.id}</span>
                <span class="text-sm text-gray-500">${download.started_at}</span>
            </div>
            <div class="mb-2">
                <div class="text-sm text-gray-600 truncate">${download.url}</div>
            </div>
            <div class="relative pt-1">
                <div class="flex mb-2 items-center justify-between">
                    <div>
                        <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full ${getStatusColor(download.status)}">
                            ${download.status}
                        </span>
                    </div>
                    <div class="text-right">
                        <span class="text-xs font-semibold inline-block text-gray-600">
                            ${download.progress}%
                        </span>
                    </div>
                </div>
                <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
                    <div style="width:${download.progress}%" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-blue-500"></div>
                </div>
            </div>
        </div>
    `).join('');

    // Update history table
    const historyBody = document.getElementById('download-history');
    historyBody.innerHTML = data.history.map(item => `
        <tr>
            <td>${item.id}</td>
            <td>${item.type}</td>
            <td class="truncate max-w-xs">${item.url}</td>
            <td>${formatOptions(item.options)}</td>
            <td>
                <span class="px-2 py-1 rounded-full text-xs ${getStatusColor(item.status)}">
                    ${item.status}
                </span>
            </td>
            <td>${item.started_at}</td>
            <td>${item.completed_at || '-'}</td>
        </tr>
    `).join('');
}

function getStatusColor(status) {
    const colors = {
        'processing': 'bg-blue-100 text-blue-800',
        'completed': 'bg-green-100 text-green-800',
        'failed': 'bg-red-100 text-red-800',
        'queued': 'bg-yellow-100 text-yellow-800',
        'cancelled': 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
}

function formatOptions(options) {
    return Object.entries(options)
        .map(([key, value]) => `${key}: ${value}`)
        .join(', ');
}

// Connect when page loads
connectWebSocket();