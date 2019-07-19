# Kintyre Speedtest Apps for Splunk

**Project name:**  Shinnecock

How often do you visit speedtest.net or ping 8.8.8.8 to test the connectivity and performance of your Internet connection?  Would it be useful to look back over time at these results?  Almost everyone has multiple devices and uses different WiFi connections. Companies manage fleets of computers and multiple office locations probably with varied telecom providers.  Splunk is a simple and practical solution to see how the Internet service you pay for, or otherwise rely upon, is working for you over time.  We have wrapped the speedtest.net CLI into a Techonlogy Add-on that can be deployed to forwarders or easily installed via an open source Python package that works with HEC to ingest data into Splunk over commonly used ports.

There is a large gap between what is available to consumers and small companies, and what is available only to companies with large investments in telecom and networking infrastructure, including the economic constraints with features.  As individuals or smaller companies who know Splunk or want a less expensive option to a very common problem, this app/TA/python package may be just the perfect fit.

**Splunk apps:**

 * [Kintyre Speedtest App for Splunk](./kintyre-speedtest) - user interface showing speedtest results
   and trends
 * [Kntyre Speedtest Add-on for Splunk](./kintyre-speedtest-TA) - Speedtest data collection for
   splunk (universal forwarder) endpoints

The Kintyre Speedtest Technology Add-on uses the standalone Shinnecock Agent to capture and collect
speedtest data.  Please visit the sibiling [Shinnecock Agent][shinnecock-agent-repo] repository for
more details including an index of the exceptional third party libraries making this possible.

## Requirements

**Kintyre Speedtest App for Splunk**:

  * Splunk Enterprise 6.5+

**Kintyre Speedtest Add-on for Splunk**

  * Splunk Enterprise or universal forwarder (UF)
  * A local python install (for universal forwarders)
  * Open outbound Internet connectivity (for collecting speed testing)

## Installation

 * Install `kintyre-speedtest` on your search head.
 * Enable/Configure HEC (if you're using any standalone agents)
 * Setup / confirm indexes
 * Install agents (Use either deploy the `kintyre-speedtest-TA` or install the standalone agent) 


## Collecting speedtest data

There are two supported methods for collecting speedtest data.  Speedtest data can be collected from
ether the Speedtest Add-on or via a standalone agent.  If your Splunk ecosystem is already well
defined and the endpoints you'd like to collect network performance data from already have universal forwarders
managed via deployment server, then using the add-on is advised.  However, if you are looking
to collect bandwidth metrics from embedded devices or a fleet of remote laptops not part of
your Splunk infrastructure, the standalone agent may be more suitable.  It's also possible to
mix and match if circumstances dictate.

_Feature comparison:_

| Category | Speedtest Add-on | Standalone Agent |
| -------- | ---------------- | -----------------|
| Targeted use | Leveraging and expanding existing Splunk infrastructure | Lightweight standalone data collection with no centralized management |
| Deployment method | A splunk app | Python package |
| Install | Deploy to endpoints via deployment server | Install python package and register agent |
| Scheduling | Set the interval via `inputs.conf` on the deployment server | Uses external mechanism like `cron` or Windows Task scheduler |
| Data forwarding | Using existing Splunk protocol (i.e., tcp/9997) | Splunk HTTP Event Collector (HEC).  Can use traditionally open ports like HTTTPS (tcp/443) |
| Python | Uses embedded python (Splunk enterprise) or OS-provided Python for Universal Forwarder | Requires OS-provided Python |
| Configuration | Minimal options.  Handled by Splunk .conf files. | More options exists.  Initial setup handle via a `register` CLI option or by editing an `.ini` file. |

The standalone agent has been tested on several Linux distributions, Windows, MacOS, and embedded
devices like the Raspberry Pi.

Note:  Technically the same python code is used for both the *Kintyre Speedtest Add-on for Splunk*
so the same data will be collected either way.  The flexibility of the standalone agent will always
exceed that of the add-on, which is geared towards a very niche deployment scenario.  Long-term we
hope to provide self-installing standalone agents to remove the need to have an existing python
deployment.



[shinnecock-agent-repo]: https://github.com/Kintyre/shinnecock-agent
