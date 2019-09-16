# NetApp ONTAP Skill for Opsdroid

This is an OPSDROID skill for ChatOps using the ONTAP SDK for Python to make it easy to interact with ONTAP's Rest API's. Opsdroid is an open source chat bot framework written in Python. It is designed to be extendable, scalable and simple.

![alt text](/img/demo.png)

## :traffic_light: Prerequisites

* `python 3.5 or later`
* `requests 2.21.0 or later`
* `marshmallow between 3.0.0rc5 and 3.0.0rc7`
* `ONTAP SDK for Python`

## :hammer: Installation

Install opsdroid from pip:

```
$ pip install opsdroid
$ pip install netapp-ontap

#run the opsdroid command to create the configuration files

$ opsdroid

# Stop opsdroid  with Ctrl + C to modify the configuration
```

## :blue_book: Configuration
Modify the opsdroid configuration.yaml file and make sure it contains the following sections: 
* Chat service e.g. Slack
* ONTAP skill added to the skills section
* Regex is enabled, for parsing messages

For configuration, opsdroid uses a single YAML file named configuration.yaml. When you run opsdroid it will look for the file in the following places in order:

* `./configuration.yaml`
* `/etc/opsdroid/configuration.yaml`
One of the default locations:
* `Mac: ~/Library/Application Support/opsdroid`
* `Linux: ~/.local/share/opsdroid` or `~/.config/opsdroid`
* `Windows: C:\<User>\<Application Data>\<Local Settings>\opsdroid\ or  C:\Users\<User>\AppData\Local\opsdroid`

Note: If no file named configuration.yaml can be found on one of these folders one will be created for you taken from the example configuration file.

If you are using one of the default locations you can run the command opsdroid -e or opsdroid --edit-config to open the configuration with your favorite editor(taken from the environment variable EDITOR) or the default editor vim.

Then add the ONTAP skill to the skill section of the opsdroid configuration.yaml file.
```
  ## Interact with ONTAP API
  - name: ontap
    repo: https://github.com/promiseowolabi/skill-ontap.git
    no-cache: True

```
Uncomment Regex for parsing in the configuration.yaml file:
```
parsers:
  - name: regex
    enabled: true
```
Setup your chat service e.g. Slack in the configuration.yaml file:
```
  - name: slack
    # required
    api-token: "your-slack-token-goes-here"
    # optional
    bot-name: "opsdroid" # default "opsdroid"
    default-room: "#chatops" # default "#general"
    icon-emoji: ":robot_face:" # default ":robot_face:"
    connect-timeout: 10 # default 10 seconds
```
Start opsdroid after you complete the configuration
```
$ opsdroid
```
## :mag: Usage

On you chosen chat service, these are some example messages based on regex_matches the skill will respond to, refer to the Quickstart documentation for a complete list:

* `get ontap cluster info`
* `get ontap cluster version`
* `get ontap cluster name`
* `create a {size} MB volume called {name} on svm {svm} and aggregate {aggr}`
* `delete volume {name} on svm {svm}`
* `get volumes on svm {svm}`
* `get all aggregates on cluster` or `get aggregates on cluster`
* `get all ports state on cluster` or `get ports state on cluster`
* `get all interfaces on cluster` or `get interfaces on cluster`
* `create a snapshot of {volume} on svm {svm}` or `take a snapshot of {volume} on svm {svm}`
* `create a clone of {volume} on svm {svm} called {name}` or `create a flexclone of {volume} on svm {svm} called {name}`

Slack: Enclose hostnames, FQDN values in < > i.e. <sqlhost.netapp.com> to avoid Slack unfurling which cause hostname not found errors.

#### Note: The messages must match the syntax above including letter cases.

## :pushpin: License

* [MIT License](LICENSE)
