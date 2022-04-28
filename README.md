# Micropresence

Bind K8S services to your local instances for development and debugging.

![Micropresence](logo.png?raw=true "Docker Compose Logo")

> micropresence : microK8S = telepresence : K8S


The tool works as a **prototipal, light-weight and very delimited alternative** to [Telepresence](https://github.com/telepresenceio/telepresence) of which it resembles the 1.0 version.
It is suited for test and debugging early stage development environment, as the ones running on microK8S:  

- Micropresence forwards K8S connections to your local running instances to ease development end debugging
- it restores original settings at the end of your development session, recovering setting in case of failure at the next start 


## Installation

Micropresence requires:

- to install in your K8S cluster a SSH server (the _bastion host_)
- `kubectl` installed and configured on your PC with a `kubeconfig` file (`~/.kube/config`)
- an SSH client configured to connect without user interaction to the bastion host (by `~/.ssh/config`)


## Usage

Install micropresence is as simple as cloning the repo and running `pip install .` or `python3 setup.py install`.

Then, check if `kubectl` and the connection to your K8S bastion are well configured:

```shell
$ microk8s.kubectl -n my-namespace get services
NAME                                 TYPE           CLUSTER-IP       EXTERNAL-IP             PORT(S)                       AGE
frv-mixol                            ClusterIP      10.152.183.82    <none>                  80/TCP                        93d
frv-elasearch                        ClusterIP      10.152.183.235   <none>                  80/TCP                        93d
frv-dromedario                       ClusterIP      10.152.183.164   <none>                  80/TCP                        93d

$ ssh frv-nightly
Welcome to OpenSSH Server

aulic-ssh-server-b886d6fc4-zf8rg:~$ wget http://frv-elasearch/my-not-found-endpoint
Connecting to frv-elasearch (10.152.183.235:80)
wget: server returned error: HTTP/1.1 404
```

Decide which service you want to swap with your local instance, let's suppose we choose `frv-mixol`:
- Start `micropresence --namespace my-namespace --ssh-connection-name frv-nightly frv-mixol:http:8080` 
- Run your local instance of `frv-mixol` on port `8080` 


You may need to bridge your network with the one of your K8S services. 
This happens if you are not running `micropresence` on the same host that is running K8S. 
In such cases, we support [sshuttle](https://github.com/sshuttle/sshuttle) by the optional parameter `--vpn`.

## Known limits

> **Micropresence is protipal, has been developed for our specific needs and demands for work to cover additional use cases.**
> Additional features are out of scope, at the moment.

Known limits of micropresence are:

- It cannot forward port to hosts different from localhost.
- It only uses the configuration from `~/.kube/config`

Contribution are welcome.

## License

Copyright 2022 
Fervento srl (https://fervento.com)

`micropresence` and all files in this repository are licensed under the Apache License, Version 2.0 (the "License").

THERE IS NO WARRANTY FOR THE USE OF MICROPRESENCE, USE AT YOUR OWN RISK!

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
 
SHOULD THE PROGRAM OR DOCUMENTATION PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
