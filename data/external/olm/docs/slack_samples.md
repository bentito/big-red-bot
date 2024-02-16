## Question 

Hi, is there any guidance available for installing an operator as a dependency in a different namespace? It'll be awesome to know of any feature that deploys an operator conditionally.
 
 
### Answer

Unfortunately, OLM only knows how to resolve dependencies for operators in the same namespace (and thus the same watch context), generally best practice is to have as few permissions on your operator as possible.

## Question 

Using OLM (Operator Lifecycle Manager), when installing an operator, how can Customer change the registry of the container image that is specified in the CSV for the operator's deployment.
I understand that things like CPU resources and environment variables can be configured on the Subscription CR. Is this possible for the image or the image registry as well?
Example use case:
I configure my CSV with a certain image:
`my-registry-a/my-operator:latest`
I create the Bundle and after that intend to I deploy it to my cluster, but I want to change the image on the operator's Deployment to (without altering the Bundle):
`my-registry-b/my-operator:latest`
Should we directly edit the CSV ?  if yes then that would eliminate the purpose of the Subscription?"


### Answer 

Hello, did they mirror the image into a different registry? The image content source policy api that we use for disconnected mirroring pretty much exists for this purpose

## Question 

Hello Team, #forum-ocp-operator-fw Can we configure the backup data protection application to run with a more restricted 
service account? The default Velero service account has near cluster admin rights and we don't want that when installing 
the operator into user namespace.  As this is deployed and managed by the OADP operator, making any changes to RBAC or 
service accounts upsets the operator and the operator status changes to 'Pending' and says 'requirements no longer met'.
Any help would be deeply appreciated.

### Answer

It's not clear to me why the container catalog UI displays that, but those index images are updated several times a day 
every day whenever a new operator version for something in our catalog gets released. The folks on this channel don't own 
those images, but have you confirmed if the latest version on that tag contains that cve or not?

## Question 

Hello #forum-ocp-operator-fw, I am not sure if this is the right place to ask this. I have a customer who is facing some issues with the configuration of webhooks associated to dynakubes for the Dynatrace operator on their ARO (Azure RedHat openshift) cluster.
1 graph_builder.go:281] garbage controller monitor not yet synced: dynatrace.com/v1beta1, Resource=dynakubes
I advised the customer to check the configuration of webhooks associated to dynakubes and follow this KCS for some guidelines: https://access.redhat.com/solutions/7005068
Customer would like to know if deleting the Dynatrace namespace / Dynatrace Operator in ARO will also delete the webhooks?
Or do they have to remove the webhooks separately from the namespace after they delete the dynatrace namespace?

### Answer 

Hey. As far as I understand from the KCS - the issue is that for some reason the server which performs CRD version conversion does not work and it causes garbage collection issues.
I highly recommend getting to the bottom of this and finding what is going on with the conversion webhook server. From knowing the cause it will be more clear what action need to be taken.
In the meantime - here is the doc on how to delete an operator. Note:
This action does not remove resources managed by the Operator, including custom resource definitions (CRDs) and custom resources (CRs). Just wanted to clarify: while OLM does not delete CRDs - it cleans up the .spec.conversion on CRDs.
So nothing will be pointing to the deleted workload (webhook server).

## Question 

Hi folks - we are trying to create an OLM bundle for a new operator and we have a role and rolebinding that we want to create in another namespace. So, we defined the role under the static-namespace  directory with a  namespace transformer. When creating the bundle, we don't see this role and rolebinding created. 
Is there something we are missing or could we add files manually into the bundle folder after the creation of the bundle?

### Answer 

I'm not an expert on kubebuilder or what the operator-sdk does with manifest directories, but this isn't something that's actually supported by olm bundles. You can drop rbac manifests into the bundle, and OLM will accept them, but it will apply roles in whatever namespace the operator is being installed in. OLM templates any of the manifests in the bundle itself so they are applied in the context of the installplan. 
It's giving the admin the control to decide "where" the operator is installed.


## Question 

#forum-ocp-operator-fw Hello Everyone, We got a cu query regarding the installation of  Dynatrace Monitoring Agent on OCP 4.8 and 4.11; I am going through the previous asks on the channel and could see that itr got installed on 4.8 also. But from the Catalog list it specifies it is supported fro supported Red Hat OpenShift 4.11, 4.12, 4.13, 4.14 -   https://catalog.redhat.com/software/container-stacks/detail/5fb374d4d85e8689c39f0877
Also, This article says it is supported   - https://access.redhat.com/solutions/6016311
Could you please help us in answering the cu query.

### Answer

You'll need to contact the maintainers of the dynatrace operator to find out if it's still supported  in OCP 4.8. You can find the maintainer contact information in the bar on the right side of this page: https://operatorhub.io/operator/oneagent

## Question 

Hello #forum-ocp-operator-fw Team,
Our customer asked they want to install  GCP spark operator [1]
We are using the following index image for source: registry.redhat.io/redhat/community-operator-index:v4.12
we run the following command to get an overview of operators available in index image:
oc-mirror list operators --catalog=registry.redhat.io/redhat/community-operator-index:v4.12
However, we cannot find the gcp-spark operator. When looking at the github repo of red hat for the community index image [2], it is listed in the list of operators .
Why is the gcp-spark operator not available using oc-mirror list operators?

1.  https://operatorhub.io/operator/spark-gcp
2. https://github.com/redhat-openshift-ecosystem/community-operators-prod/tree/main/operators
If this is not the correct forum please let me the respective forum to raise this query.

### Answer 

https://github.com/redhat-openshift-ecosystem/community-operators-prod/blob/main/operators/spark-gcp/2.4.0/metadata/annotations.yaml#L8 looks like the last version pushed to the downstream community was for ocp 4.8 and it hasn't been maintained in a long time. 
The crd is still v1beta1 which was removed from kube all the way back in 1.20. 

## Question 

 We were looking at potentially adding the ci-operator to our OLM operator setup. 
 I have the following documentation but I'm trying to get clarity on what steps I'd have to take in Github to get thing enabled. Any help would be appreciated. 
 
 ### Answer 
 
This might be a better question for the dptp folks in #forum-ocp-testplatform
 
 ## Question 
 
Hey, looking for guidance on how to do Tier 2 support for operators with both a rolling update strategy and a per-y-stream strategy.
eg., can we do both a stable channel and a set of stable-1.1 , stable-1.2, stable-1.3 channels...
and does that mean building 2 bundles per release, and 2 erratas per release?

### Answer 

You're definitely going to want to avoid a channel called stable (what happens when you need to release a v2?). It would be better to call it stable-v1.
Other than that, what you're describing sounds a lot like the file-based catalog ""semver template"" https://olm.operatorframework.io/docs/reference/catalog-templates/#semver-template


## Question 

Hello, I am working with opm to get CSV from bundle container with opm render .... With version 1.26 I was able to get all data in base64, decode it and get for example Deployment for the operator. However, with 1.28 and newer versions it seems I get only CSV metadata. Is there a way how to achieve the same behavior as I did with 1.26? Maybe there is some misconfiguration in our bundle metadata?  Thanks!
From my understanding this is the reason for the behavior change - https://github.com/operator-framework/operator-registry/pull/1094

### Answer

If you are using opm render directly on bundle images, there is no way to get CSV data as of 1.28.
opm render is for rendering  catalogs/catalog metadata from bundles, not bundles directly.
In the past, it was necessary to include the full CSV in the catalog in order for OLM to serve its packagemanifests API. Now, we have significantly reduced the amount of data necessary to include in the catalog to be able to continue serving that API.
You have two options:
Use the new olm.csv.metadata property in the catalog, which contains a subset of the CSV fields.
Extract the bundle images directly and read their /manifests directory. (OLM afaik does not have an official tool for this). However, check out: https://github.com/exdx/dcp