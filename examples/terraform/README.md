# policy_sentry-terraform-example

Example of using [policy_sentry](https://github.com/salesforce/policy_sentry) with Terraform to generate secure policies automagically.

## Prerequisites

This requires:
* Terraform v0.12.8
* AWS credentials; must be authenticated

## Demo

* Install policy_sentry

```bash
pip3 install policy_sentry
```

* Initialize policy_sentry

```bash
policy_sentry initialize
```

* Execute the first Terraform module:

```bash
cd environments/standard-resources
tfjson install 0.12.8
terraform init
terraform plan
terraform apply -auto-approve
```

This will create a YML file to be used by policy_sentry in the [environments/iam-resources/files/](environments/iam-resources/files/) directory titled [example-role-randomid.yml](environments/iam-resources/files/example-role-jpwdp.yml).

* Write the policy using policy_sentry:

```bash
cd ../iam-resources
policy_sentry write-policy-dir --crud --input-dir files --output-dir files
```

This will create a JSON file to be consumed by Terraform's `aws_iam_policy` resource to create an IAM policy.

* Now create the policies with Terraform:

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

* Don't forget to cleanup

```bash
terraform destroy -auto-approve
cd ../standard-resources
terraform destroy -auto-approve
```

## Using the Terraform modules in your code

#### Step 1: Install policy_sentry

* Install policy_sentry

```bash
pip3 install -r requirements.txt
```

* Initialize policy_sentry

```bash
policy_sentry initialize
```


#### Step 2: Generate the policy_sentry YAML File
Create a file with the following in `some-directory`:

```hcl-terraform
module "policy_sentry_yml" {
  source           = "git::https://github.com/salesforce/policy_sentry.git//examples/modules/generate-policy_sentry-yml"
  role_name        = ""
  role_description = ""
  role_arn         = ""

  list_access_level                   = []
  permissions_management_access_level = []
  read_access_level                   = []
  tagging_access_level                = []
  write_access_level                  = []

  yml_file_destination_path = "../other-directory/files"
}
```

Make sure you fill out the actual directory path properly. Note that `yml_file_destination_path` should point to the directory mentioned in Step 3.

#### Step 3: Run policy_sentry and specify proper target directory

* Enter the directory you specified under `yml_file_destination_path` above.

* Run the following:

```bash
policy_sentry write-policy-dir --crud --input-dir files --output-dir files
```

#### Step 4: Create the IAM Policies using JSON files from directory

Then from `other-directory`:

```hcl-terraform
module "policies" {
  source = "git::https://github.com/salesforce/policy_sentry.git//examples/terraform/modules/generate-iam-policies"
  relative_path_to_json_policy_files = "files"
}
```
