#!/usr/bin/python
__metaclass__ = type

# Manage ZFS datasets.

# XXX
DOCUMENTATION = '''
---
module: dataset
short_description: Manage ZFS datasets
description: 
options:
  name:
    - 
'''

# XXX
EXAMPLES = '''
'''

# XXX
RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.arensb.truenas.plugins.module_utils.middleware \
    import MiddleWare as MW


def main():
    # XXX - from pool.dataset.create:
    # - name (str)
    # - type: {FILESYSTEM, VOLUME}
    # - volsize (int)
    # - volblocksize: {512, 1K, 2K, 4K, 8K, 16K, 32K, 64K, 128K}
    # - sparse (bool)
    # - force_size (bool)
    # - comments (str)
    # - sync: {STANDARD, ALWAYS, DISABLED}
    # - compression: {OFF, LZ4, GZIP, GZIP-1, GZIP-9, ZSTD, LZJB, ...}
    # - atime: {ON, OFF}
    # - exec: {ON, OFF}
    # - managedby (str)
    # - quota (int or null)
    # - quota_warning (int)
    # - quota_critical (int)
    # - refquota (int or null)
    # - refquota_warning (int)
    # - refquota_critical (int)
    # - reservation (int)
    # - refreservation (int)
    # - special_small_block_size (int)
    # - copies (int)
    # - snapdir {VISIBLE, HIDDEN}
    # - dedupliation {ON, VERIFY, OFF}
    # - checksum {ON, OFF, FLETCHER{2,4}, SHA{256,512}, SKEIN}
    # - readonly {ON, OFF}
    # - recordsize (str)
    # - casesensitivity {SENSITIVE, INSENSITIVE, MIXED}
    # - aclmode {PASSTHROUGH, RESTRICTED}
    # - acltype {NOACL, NFS4ACL, POSIXACL}
    # - share_type {GENERIC, SMB}
    # - xattr {ON, SA}
    # - encryption_options (obj):
    #   - generate_key (bool)
    #   - pbkdf2iters (int)
    #   - algorithm {AES-*-CCM}
    #   - passphrase (str or null)
    #   - key (str or null)
    # - encryption (bool)
    # - inherit_encryption (bool)
    module = AnsibleModule(
        argument_spec=dict(
            # XXX
            name=dict(type='str'),
            ),
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        msg=''
    )

    mw = MW()

    # Assign variables from properties, for convenience
    name = module.params['name']
    # XXX

    # XXX - Look up the resource
    try:
        resource_info = mw.call("resource.query",
                                [["name", "=", name]])
        if len(resource_info) == 0:
            # No such resource
            resource_info is None
        else:
            # Resource exists
            resource_info = resource_info[0]
    except Exception as e:
        module.fail_json(msg=f"Error looking up resource {name}: {e}")

    # First, check whether the resource even exists.
    if resource_info is None:
        # Resource doesn't exist

        if state == 'present':
            # Resource is supposed to exist, so create it.

            # Collect arguments to pass to resource.create()
            arg = {
                "resourcename": name,
            }

            if feature is not None and:
                arg['feature'] = feature

            if module.check_mode:
                result['msg'] = f"Would have created resource {name} with {arg}"
            else:
                #
                # Create new resource
                #
                try:
                    err = mw.call("resource.create", arg)
                    result['msg'] = err
                except Exception as e:
                    result['failed_invocation'] = arg
                    module.fail_json(msg=f"Error creating resource {name}: {e}")

                # Return whichever interesting bits resource.create()
                # returned.
                result['resource_id'] = err

            result['changed'] = True
        else:
            # Resource is not supposed to exist.
            # All is well
            result['changed'] = False

    else:
        # Resource exists
        if state == 'present':
            # Resource is supposed to exist

            # Make list of differences between what is and what should
            # be.
            arg = {}

            if feature is not None and resource_info['feature'] != feature:
                arg['feature'] = feature

            # If there are any changes, resource.update()
            if len(arg) == 0:
                # No changes
                result['changed'] = False
            else:
                #
                # Update resource.
                #
                if module.check_mode:
                    result['msg'] = f"Would have updated resource {name}: {arg}"
                else:
                    try:
                        err = mw.call("resource.update",
                                      resource_info['id'],
                                      arg)
                    except Exception as e:
                        module.fail_json(msg=f"Error updating resource {name} with {arg}: {e}")
                        # Return any interesting bits from err
                        result['status'] = err['status']
                result['changed'] = True
        else:
            # Resource is not supposed to exist

            if module.check_mode:
                result['msg'] = f"Would have deleted resource {name}"
            else:
                try:
                    #
                    # Delete resource.
                    #
                    err = mw.call("resource.delete",
                                  resource_info['id'])
                except Exception as e:
                    module.fail_json(msg=f"Error deleting resource {name}: {e}")
            result['changed'] = True

    module.exit_json(**result)


# Main
if __name__ == "__main__":
    main()