// ======================================================
// SmartReco Behavior Tracker
// ======================================================

// Generate a browser session

let sessionId = localStorage.getItem("smartreco_session");

if (!sessionId) {

    sessionId = crypto.randomUUID();

    localStorage.setItem(
        "smartreco_session",
        sessionId
    );
}

// ======================================================
// Event Queue
// ======================================================

const eventQueue = [];

function sendEvent(
    eventType,
    eventData = {}
) {

    eventQueue.push({

        session_id: sessionId,

        event_type: eventType,

        event_data: eventData,

        timestamp:
            new Date().toISOString()

    });

}

// ======================================================
// Flush Events Every 5 Seconds
// ======================================================

async function flushEvents() {

    if (eventQueue.length === 0) {
        return;
    }

    const events = [...eventQueue];

    eventQueue.length = 0;

    try {

        await fetch(
            "/behavior/batch",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    events: events
                }),
            }
        );

    } catch (err) {

        console.error(err);

    }

}

setInterval(
    flushEvents,
    5000
);

// ======================================================
// Session Start
// ======================================================

sendEvent(
    "session_start",
    {
        page: window.location.pathname
    }
);

// ======================================================
// Page View
// ======================================================

sendEvent(
    "page_view",
    {
        page: window.location.pathname
    }
);

// ======================================================
// Product View
// ======================================================

if (window.PRODUCT_ID) {

    sendEvent(
        "product_view",
        {
            product_id: window.PRODUCT_ID
        }
    );

}

// ======================================================
// Search
// ======================================================

const searchForm =
    document.querySelector("form");

if (searchForm) {

    searchForm.addEventListener(
    "submit",
    function () {

        const input =
            document.querySelector(
                "input[name='query']"
            );

        if (input && input.value.trim() !== "") {

            sendEvent(

                "search",

                {

                    query: input.value.trim(),

                    page: window.location.pathname,

                }

            );

        }

    }
);

}

// ======================================================
// Click Tracking
// ======================================================

document.addEventListener(
    "click",
    function (e) {

        const target =
            e.target.closest("a");

        if (!target) {

            return;

        }

        sendEvent(
            "click",
            {
                href: target.href,
                text: target.innerText
            }
        );

    }
);

// ======================================================
// Session End
// ======================================================

window.addEventListener(
    "beforeunload",
    function () {

        navigator.sendBeacon(

            "/behavior/event",

            new Blob(

                [

                    JSON.stringify({

                        session_id: sessionId,

                        event_type: "session_end",

                        event_data: {

                            page:
                                window.location.pathname

                        },

                        timestamp:
                            new Date().toISOString()

                    })

                ],

                {

                    type:
                        "application/json"

                }

            )

        );

    }
);