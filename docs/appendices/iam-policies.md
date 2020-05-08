IAM Policies
============

This document covers:

-   Elements of an IAM Policy
-   Breakdown of the tables for Actions, Resources, and Condition keys
    per service
-   Generally how policy_sentry uses these tables to generate IAM
    Policies

IAM Policy Elements
-------------------

The following IAM JSON Policy elements are included in
policy_sentry-generated IAM Policies:

-   [Version](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_version.html):
    specifies policy language versions dictated by AWS. There are two
    options - `2012-10-17` and `2008-10-17`. policy_sentry generates
    policies for the most recent policy language - `2012-10-17`
-   [Statement](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_statement.html):
    There is one **statement array** per policy, with multiple
    statements/SIDs inside that statement. The elements of a single
    statement/SID are listed below.
    -   [SID](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_sid.html):
        Statement ID. Optional identifier for the policy statement. SID
        values can be assigned to each statement in a statement array.
    -   [Effect](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_effect.html):
        `Allow` or explicit `Deny`. If there is any overlap on an action
        or actions with Allow vs. Deny, the `Deny` effect overrides the
        `Allow`.
    -   [Action](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_action.html):
        This refers to the IAM action - i.e., `s3:GetObject`, or
        `ec2:DescribeInstances`. Action text in a statement can have
        wildcards included: for example, `ec2:*` covers all EC2 actions,
        and `ec2:Describe*` covers all EC2 actions prefixed with
        `Describe` - such as `DescribeInstances`,
        `DescribeInstanceAttributes`, etc.
    -   [Resource](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html):
        This refers to an Amazon Resource Name (ARN) that the Action can
        be performed against. There are differences in ARN format per
        service. Those differences can be viewed [in the AWS Docs on
        ARNs and
        Namespaces](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)

The ones we don't use in this tool:

-   [Condition](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html)
    (will be added in a future release)
-   [Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html)
-   [NotPrincipal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notprincipal.html)
-   [NotResource](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notresource.html)

Actions, Resources, and Condition Keys Per Service
--------------------------------------------------

This documentation is the seed source for the database that we create in
policy_sentry. It contains tables for **(1) Actions**, **(2)
Resources/ARNs**, and **(3) Condition Keys** for each service. This
documentation is of critical importance because **every IAM action for
every IAM service has different ARNs that it can apply to, and different
Condition Keys that it can apply to.**

### Action Table

Consider the Action table snippet from KMS shown below (source
documentation can be viewed [on the KMS documentation
here](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awskeymanagementservice.html#awskeymanagementservice-actions-as-permissions)).


<table border="1" class="docutils">
<colgroup>
<col width="22%" />
<col width="21%" />
<col width="17%" />
<col width="17%" />
<col width="23%" />
</colgroup>
<tbody valign="top">
<tr class="row-odd"><td><strong>Actions</strong></td>
<td><strong>Access Level</strong></td>
<td><strong>Resource Types</strong></td>
<td><strong>Condition Keys</strong></td>
<td><strong>Dependent Actions</strong></td>
</tr>
<tr class="row-even"><td rowspan="2">kms:CreateGrant</td>
<td rowspan="2">Permissions management</td>
<td>key*</td>
<td>&#160;</td>
<td>&#160;</td>
</tr>
<tr class="row-odd"><td><ul class="first last simple">
<li></li>
</ul>
</td>
<td>kms:CallerAccount</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>kms:CreateCustomKeyStore</td>
<td>Write</td>
<td><ul class="first last simple">
<li></li>
</ul>
</td>
<td>&#160;</td>
<td>cloudhsm:DescribeClusters</td>
</tr>
</tbody>
</table>


As you can see, the Actions Table contains these columns:

-   **Actions**: The name of the IAM Action
-   **Access Level**: how the action is classified. This is limited to
    List, Read, Write, Permissions management, or Tagging.
    -   This classification can help you understand the level of access
        that an action grants when you use it in a policy.
    -   For more information about access levels, see [Understanding
        Access Level Summaries Within Policy
        Summaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_understand-policy-summary-access-level-summaries.html).
-   **Condition Keys**: The condition key available for that action.
    There are some service specific ones that will contain the service
    namespace (i.e., `ec2`, or in this case, `kms`. Sometimes, there are
    AWS-level condition keys that are available to only some actions
    within some services, such as
    [aws:SourceAccount](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourceaccount).
    If those are available to the action, they will be supplied in that
    column.
-   **Dependent Actions**: Some actions require that other actions can
    be executed by the IAM Principal. The example above indicates that
    in order to call `kms:CreateCustomKeyStore`, you must be able to
    also execute `cloudhsm:DescribeClusters`.

**And most importantly** to the context of this tool, there is the
Resource Types column:

-   **Resource Types**: This indicates whether the action supports
    resource-level permissions - i.e., *restricting IAM Actions by ARN*.
    If there is a value here, it points to the ARN Table shown later in
    the documentation.
    -   In the example above, you can see that
        `kms:CreateCustomKeyStore`'s Resource Types cell is blank; this
        indicates that `kms:CreateCustomKeyStore` can **only** have `*`
        as the resource type.
    -   Conversely, for `kms:CreateGrant`, the action can have
        either (1) `*` as the resource type, or `key*` as the resource
        type. The ARN format is not actually `key*`, it just points to
        that ARN format in the ARN Table explained below.

### ARN Table

Consider the KMS ARN Table shown below (the source documentation can be
viewed [on the AWS website
here](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awskeymanagementservice.html#awskeymanagementservice-resources-for-iam-policies).

  -------------- ------------------------------------------------------------ --------------
  **Resource     **ARN**                                                      **Condition
  Types**                                                                     Keys**

  alias          `arn:${Partition}:kms:${Region}:${Account}:alias/${Alias}`

  key            `arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}`
  -------------- ------------------------------------------------------------ --------------

The ARN Table has three fields:

-   **Resource Types**: The name of the resource type. This corresponds
    to the "Resource Types" field in the Action table. In the example
    above, the types are:

> -   `alias`
> -   `key`

-   **ARN**: This shows the required ARN format that can be specified in
    IAM policies for the IAM Actions that allow this ARN format. In the
    example above the ARN types are:

> -   `arn:${Partition}:kms:${Region}:${Account}:alias/${Alias}`
> -   `arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}`

-   **Condition Keys**: This specifies condition context keys that you
    can include in an IAM policy statement only when both (1) this
    resource and (2) a supporting action from the table above are
    included in the statement.

### Condition Keys Table

There is also a Condition Keys table. An example is shown below.

  -------------------------------------- ---------- ---------------------------------------------------------
  **Condition Keys**                     **Type**   **Description**

  `kms:BypassPolicyLockoutSafetyCheck`   Bool       Controls access to the CreateKey and PutKeyPolicy
                                                    operations based on the value of the
                                                    BypassPolicyLockoutSafetyCheck parameter in the request.

  `kms:CallerAccount`                    String     Controls access to specified AWS KMS operations based on
                                                    the AWS account ID of the caller. You can use this
                                                    condition key to allow or deny access to all IAM users
                                                    and roles in an AWS account in a single policy statement.
  -------------------------------------- ---------- ---------------------------------------------------------

**Note**: While policy_sentry does import the Condition Keys table into
the database, it does not currently provide functionality to insert
these condition keys into the policies. This is due to the complexity of
each condition key, and the dubious viability of mandating those
condition keys for every IAM policy.

We might support the Global Condition keys for IAM policies in the
future, perhaps to be supplied via a user config file, but that
functionality is not on the roadmap at this time. For more information
on Global Condition Keys, see [this
documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#AvailableKeys).

### References

-   [ARN Formats and Service
    Namespaces](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)
-   [IAM Policy
    Elements](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)
-   [IAM Actions, Resources, and Context Keys per
    service](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html)
-   [Actions Table
    explanation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html#actions_table)
-   [ARN Table
    explanation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html#resources_table)
-   [Condition Keys Table
    explanation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html#context_keys_table)
-   [Global Condition
    Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#AvailableKeys)
