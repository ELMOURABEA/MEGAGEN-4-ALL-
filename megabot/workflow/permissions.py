"""
Permission management system
"""
from typing import Dict, Any, List, Set
from enum import Enum


class PermissionLevel(Enum):
    """Permission levels for operations"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    FULL = "full"


class PermissionManager:
    """Manages permissions for different operations"""
    
    def __init__(self, default_level: str = "full"):
        """
        Initialize permission manager
        
        Args:
            default_level: Default permission level
        """
        self.default_level = default_level
        self.permissions: Dict[str, Set[str]] = {
            "database": set(),
            "api": set(),
            "workflow": set(),
            "research": set()
        }
        
        # Set default permissions based on level
        self._set_default_permissions(default_level)
    
    def _set_default_permissions(self, level: str):
        """Set default permissions based on level"""
        if level == "full":
            for resource in self.permissions:
                self.permissions[resource] = {
                    PermissionLevel.READ.value,
                    PermissionLevel.WRITE.value,
                    PermissionLevel.EXECUTE.value,
                    PermissionLevel.ADMIN.value
                }
        elif level == "admin":
            for resource in self.permissions:
                self.permissions[resource] = {
                    PermissionLevel.READ.value,
                    PermissionLevel.WRITE.value,
                    PermissionLevel.EXECUTE.value
                }
        elif level == "write":
            for resource in self.permissions:
                self.permissions[resource] = {
                    PermissionLevel.READ.value,
                    PermissionLevel.WRITE.value
                }
        else:  # read only
            for resource in self.permissions:
                self.permissions[resource] = {PermissionLevel.READ.value}
    
    def has_permission(self, resource: str, permission: str) -> bool:
        """
        Check if permission exists for resource
        
        Args:
            resource: Resource name (database, api, workflow, research)
            permission: Permission level to check
            
        Returns:
            True if permission exists
        """
        if resource not in self.permissions:
            return False
        
        # Full permission grants all
        if PermissionLevel.FULL.value in self.permissions[resource]:
            return True
        
        return permission in self.permissions[resource]
    
    def grant_permission(self, resource: str, permission: str):
        """Grant a permission for a resource"""
        if resource in self.permissions:
            self.permissions[resource].add(permission)
    
    def revoke_permission(self, resource: str, permission: str):
        """Revoke a permission for a resource"""
        if resource in self.permissions and permission in self.permissions[resource]:
            self.permissions[resource].remove(permission)
    
    def get_permissions(self, resource: str) -> List[str]:
        """Get all permissions for a resource"""
        return list(self.permissions.get(resource, set()))
    
    def check_database_access(self) -> bool:
        """Check if database access is allowed"""
        return self.has_permission("database", PermissionLevel.READ.value)
    
    def check_api_access(self) -> bool:
        """Check if API access is allowed"""
        return self.has_permission("api", PermissionLevel.EXECUTE.value)
    
    def check_workflow_execution(self) -> bool:
        """Check if workflow execution is allowed"""
        return self.has_permission("workflow", PermissionLevel.EXECUTE.value)
    
    def check_research_access(self) -> bool:
        """Check if research operations are allowed"""
        return self.has_permission("research", PermissionLevel.READ.value)
